'''
Что стоит учитывать:
- Сокращения. Можно написать код, чтобы оно занёс всевозможные сокращения от показателей
- Строчные/прописные буквы
- Одинаковые английские и русские буквы (икс = х и тд)

'''


import Levenshtein
import re

def parse_indicators_file(file_path):
    indicators = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    in_indicators_section = False
    in_units_section = False

    current_indicator = None

    for line in lines:
        line = line.strip()

        if line == "Показатель":
            in_indicators_section = True
            in_units_section = False
            continue

        if line == "Единицы":
            in_indicators_section = False
            in_units_section = True
            continue

        if in_indicators_section and line:
            current_indicator = line.split(';')[0].lower()
            indicators[current_indicator] = None

        if in_units_section and line and current_indicator:
            indicators[current_indicator] = line

    return indicators

def parse_data_file(file_path):
    data = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip().lower()
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    return data

def find_best_match(word, candidates):
    best_match = min(candidates, key=lambda candidate: Levenshtein.distance(word, candidate))
    return best_match

def extract_value_and_unit(value_str):
    match = re.match(r"([\d\.,]+)\s*(.*)", value_str)
    if match:
        number = match.group(1)
        unit = match.group(2).strip()
        return number, unit
    return value_str, ""

def compare_files(indicators_file, data_file):
    indicators = parse_indicators_file(indicators_file)
    data = parse_data_file(data_file)

    errors = []
    results = []

    for key in data:
        best_match = find_best_match(key, indicators.keys())
        expected_unit = indicators[best_match]

        value = data[key]
        number, unit = extract_value_and_unit(value)

        if expected_unit and unit != expected_unit:
            errors.append(f"Ошибка в '{key}': ожидалось '{expected_unit}', получено '{unit}'")

        results.append(f"{best_match} - {number} - {unit}")

    return errors, results

indicators_file_path = 'benchmark/indicators.txt'
data_file_path = 'benchmark/data.txt'

errors, results = compare_files(indicators_file_path, data_file_path)

if errors:
    print("Обнаружены ошибки:")
    for error in errors:
        print(error)
else:
    print("Ошибок не обнаружено.")

print("\nИтоговый вывод:")
for result in results:
    print(result)

