'''
Обязательно:
    1) Для этого вначале определить заголовок таблицы
    2) Анализ из каких столбцов состоит таблица
    Может быть, переставлены местами "единицы измерения" и "результат", например.
    3) Сравнить параметры анализов со словарем
    3.1) Учитывать возможность опечаток
    3.2) Проверять, правильно ли распознаны результаты.
         Для этого сравнивать порядки чисел результата и столбца "норма"

Дополнительно:
    1) Определение, где находятся заголовки
    2) Извлечение информации о пациенте
'''


import re
import json
import spacy
from fuzzywuzzy import process
from spacy.matcher import PhraseMatcher
import csv


nlp = spacy.load("ru_core_news_lg")

class MedicalReportProcessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.param_dict = self._load_parameters(csv_path)
        self.nlp = spacy.load("ru_core_news_lg")

    def _load_parameters(self, csv_path):
      param_dict = {}
      try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
          reader = csv.DictReader(file, delimiter=';')
          for row in reader:
            param_dict[row["Параметр"].lower()] = row
      except KeyError as e:
        print(f"Ошибка: отсутствует ключ {e} в строке CSV.")
      return param_dict



    def _setup_nlp_components(self):
        """Настройка NLP компонентов для обработки"""
        # Инициализация PhraseMatcher для медицинских терминов
        self.matcher = PhraseMatcher(self.nlp.vocab)
        patterns = [self.nlp.make_doc(param) for param in self.param_dict.keys()]
        self.matcher.add("MEDICAL_PARAMS", patterns)

        # Настройка правил для извлечения информации о пациенте
        if "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler")
        else:
            ruler = self.nlp.get_pipe("entity_ruler")

        patterns = [
            {"label": "PATIENT", "pattern": [{"LOWER": {"IN": ["пациент", "фио"]}}]},
            {"label": "BIRTHDATE", "pattern": [{"LOWER": "дата"}, {"LOWER": "рождения"}]},
            {"label": "STUDY_DATE", "pattern": [{"LOWER": "дата"}, {"LOWER": "исследования"}]}
        ]
        ruler.add_patterns(patterns)

    def extract_patient_info(self, text):
        """Извлечение информации о пациенте с использованием NLP"""
        doc = self.nlp(text)
        patient_info = {}

        for ent in doc.ents:
            if ent.label_ == "PATIENT":
                # Извлекаем текст после сущности "пациент"
                patient_text = doc[ent.end:].text
                if ":" in patient_text:
                    patient_info["Пациент"] = patient_text.split(":")[-1].strip()
                else:
                    patient_info["Пациент"] = patient_text.strip()
            elif ent.label_ == "BIRTHDATE":
                date_text = doc[ent.end:].text
                if ":" in date_text:
                    patient_info["Дата рождения"] = date_text.split(":")[-1].strip()
            elif ent.label_ == "STUDY_DATE":
                date_text = doc[ent.end:].text
                if ":" in date_text:
                    patient_info["Дата исследования"] = date_text.split(":")[-1].strip()

        return patient_info

    def process_report(self, text):
        """Основной метод обработки медицинского отчета"""
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Извлечение информации о пациенте
        patient_info = self.extract_patient_info("\n".join(lines))

        # Поиск и обработка результатов анализов
        results = []
        for line in lines:
            # Пропускаем строки с заголовками
            if any(word in line.lower() for word in ["наименование", "показатель", "результат", "единиц"]):
                continue

            # Разбор строки с результатом
            match = re.match(r"(.+?)\s+([\d,.]+)\s+([^\d\s]+)$", line)
            if match:
                name, value, unit = match.groups()
                value = value.replace(",", ".")
                matched_param = self._match_parameter(name.strip(), value, unit.strip())
                if matched_param:
                    results.append(matched_param)

        return {
            "patient_info": patient_info,
            "tests": results
        }

    def _match_parameter(self, name, value, unit):
        """Сопоставление параметра с базой данных"""
        try:
            # Лемматизация названия параметра
            doc = self.nlp(name.lower())
            lemmatized = " ".join([token.lemma_ for token in doc if not token.is_punct])

            # Поиск точного совпадения
            if lemmatized in self.param_dict:
                param_data = self.param_dict[lemmatized]
            else:
                # Поиск похожих параметров
                matches = process.extract(lemmatized, self.param_dict.keys(), limit=1)
                if not matches or matches[0][1] < 75:
                    return None
                param_data = self.param_dict[matches[0][0]]

            # Проверка единиц измерения
            expected_unit = str(param_data["Единицы измерения"]).strip().lower()
            if process.fuzz.ratio(unit.lower(), expected_unit) < 70:
                return None

            # Проверка значения
            try:
                value_num = float(value)
                ref_range = str(param_data["Норма"]).strip()

                # Проверка диапазона
                if "-" in ref_range:
                    bounds = [float(x) for x in re.findall(r"[\d.]+", ref_range)]
                    is_normal = (len(bounds) == 2 and bounds[0] <= value_num <= bounds[1])
                else:
                    try:
                        exact_val = float(ref_range)
                        is_normal = abs(value_num - exact_val) < 0.1 * exact_val
                    except ValueError:
                        is_normal = True

                return {
                    "parameter": param_data["Параметр"],
                    "value": value,
                    "unit": unit,
                    "is_normal": is_normal,
                    "reference_range": ref_range,
                    "confidence": matches[0][1] if 'matches' in locals() else 100
                }
            except ValueError:
                return None
        except Exception as e:
            print(f"Ошибка при сопоставлении параметра {name}: {str(e)}")
            return None

try:
    # Инициализация процессора с указанием пути к CSV
    processor = MedicalReportProcessor("blood_parameters.csv")

    # Пример текста медицинского отчета
    recognized_text = """
Лейкоцитарная формула при микроскопии окрашенного препарата
Пациент: Иванов Иван Иванович
Дата рождения: 01.01.1980
Дата исследования: 15.05.2023

Наименование показателя    Результат    Единицы измерения
Витамин C (аскорбиновая кислота)    10.0    мкг/мл
Витамин D общий    30.0    нг/мл
Тиамин    2.09    нг/мл
"""

    # Обработка отчета и вывод результата
    report = processor.process_report(recognized_text)
    print(json.dumps(report, ensure_ascii=False, indent=2))

except Exception as e:
    print(f"Ошибка: {str(e)}")
