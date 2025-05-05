from slovary_file import read_csv_file

"""
def correct_text(input_text, dictionary):
    
    def distance(a, b):
        n, m = len(a), len(b)
        if n == 0:
            return m
        if m == 0:
            return n

        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add = previous_row[j] + 1
                delete = current_row[j - 1] + 1
                change = previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    # Разделяем входной текст на фразы 
    phrases = input_text.split('. ')
    corrected_phrases = []

    for phrase in phrases:
        # Находим наиболее близкую фразу из словаря
        closest_phrase = min(dictionary, key=lambda dict_phrase: distance(phrase.lower(), dict_phrase.lower()))
        dist = distance(phrase.lower(), closest_phrase.lower())

        # Если расстояние меньше или равно 3, заменяем фразу
        if dist <= 3:
            corrected_phrases.append(closest_phrase)
        else:
            corrected_phrases.append(phrase)

    return '. '.join(corrected_phrases)
"""
def correct_text(input_text, dictionaries):
    
    def distance(a, b):
        n, m = len(a), len(b)
        if n == 0:
            return m
        if m == 0:
            return n

        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = list(range(n + 1))
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add = previous_row[j] + 1
                delete = current_row[j - 1] + 1
                change = previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    # Разделяем входной текст на фразы 
    phrases = input_text.split('. ')
    corrected_phrases = []

    for phrase in phrases:
        closest_phrase = None
        min_distance = float('inf')

        # Проверяем каждое слово в каждом словаре
        for dictionary in dictionaries:
            for dict_phrase in dictionary:
                dist = distance(phrase.lower(), dict_phrase.lower())
                if dist < min_distance:
                    min_distance = dist
                    closest_phrase = dict_phrase

        # Если расстояние меньше или равно 3, заменяем фразу
        if min_distance <= 3 and closest_phrase is not None:
            corrected_phrases.append(closest_phrase)
        else:
            corrected_phrases.append(phrase)

    return '. '.join(corrected_phrases)


def split_dictionary(dictionary):
    unique_words = set()

    for item in params_achive_norms[0]:
        words = item.split()
        unique_words.update(words)
        
    return unique_words

dictionary1 = ['абдоминальный', 'абсцесс', 'агглютинация', 'агнозия', 'аденома', 'адреналин', 'акклиматизация', 'акромегалия', 'аку́стика', 'аллергия', 'анемия', 'анестезия',
               'ангиография', 'ангиопатия', 'антибиотик', 'антиген', 'антидот', 'апоптоз', 'артериосклероз', 'асфиксия', 'астма', 'аудометрия', 'бактерия', 'бензодиазепин',
               'бета-адреноблокатор', 'билирубин', 'биопсия', 'блокада', 'больница', 'брадикардия', 'вакцинация', 'вегетативная система', 'вирус', 'воспаление', 'восстановление',
               'врач', 'гемоглобин', 'геморрой', 'гепатит', 'гипертония', 'гипотония', 'гистология', 'глаукома', 'грудная клетка', 'грудная жаба', 'диабет', 'диагностика',
               'диарея', 'диспноэ', 'дисфункция', 'доказательная медицина', 'долговечность', 'дозировка', 'другие болезни', 'жировая эмболия', 'заболевание', 'заболевание сердца',
               'заболевание легких', 'заживление', 'застойная сердечная недостаточность', 'злокачественная опухоль', 'зубной врач', 'зуд', 'иммунитет', 'иммунизация', 'инфекция',
               'инсульт', 'интервенция', 'исследование', 'искусственная вентиляция легких', 'калипсоидный синдром', 'канцерогенез', 'кардиограмма', 'кардиомиопатия', 'катетеризация',
               'клинические испытания', 'клиника', 'коллапс', 'коллагенозы', 'кома', 'консультация врача', 'костная ткань', 'криптозоология', 'кровотечение', 'кровяное давление',
               'крупозная пневмония', 'лаборатория', 'лекарство', 'лимфома', 'лечение', 'медицинская помощь', 'медицинская сестра', 'медицинский институт', 'метаболизм',
               'микробиология', 'миопия', 'молекулярная биология', 'муковисцидоз', 'наследственность', 'недостаточность', 'нейропатия', 'обезболивание', 'обследование', 'обструкция',
               'онкология', 'остеопороз', 'остеохондрит', 'отек', 'отравление', 'патология', 'педиатрия', 'первичная профилактика', 'периферическая нервная система', 'плазма', 'пневмония',
               'психосоматика', 'радиотерапия', 'реабилитация', 'рецидив', 'резекция', 'симптом', 'синдром', 'склероз', 'состояние здоровья', 'спазм', 'способы лечения', 'стенокардия',
               'стресс', 'суппозиторий', 'схема лечения', 'таблетка', 'терапия', 'токсикология', 'травма', 'тромбоциты', 'туберкулез', 'ультразвук', 'урология', 'фармакология',
               'физиотерапия','функция','химиотерапия','хирургия','хронический бронхит','целебные травы','эндокринология','эпидемиология']


dictionary2 = ['Аланинаминотрансфераза','АЛТ','Анемия', 'Антитела', 'Абсцесс', 'Аспартатаминотрансфераза','АСТ', 'Билирубин', 'Витамин D', 'Гамма-глутамилтрансфераза','ГГТ', 'Гемоглобин',
               'Глюкоза', 'Индекс протромбин', 'Иммуноглобулины', 'Кальций', 'Кетоны в моче', 'Креатинин',
               'Лактат', 'Лейкоциты', 'Магний', 'Натрий', ' СОЭ', 'Сахар', 'С-реактивный белок ', 'Т3 свободный',
               'Т4 свободный', 'ТТГ', 'Ферритин', 'Фосфор', 'Щелочная фосфатаза', 'Эритроциты', 'Холестерин', 'Триглицериды' ]




params_achive_norms = read_csv_file('params_archive_norms.csv', columns_to_extract=[2, 3, 4, 5])
params_achive_names = read_csv_file('params_archive_names.csv', columns_to_extract=[2, 3, 4])
genetics_parameters = read_csv_file('genetics_parameters.csv', columns_to_extract=[2, 3, 4, 5])
genetics_researches = read_csv_file('genetics_researches.csv', columns_to_extract=[2, 3, 4])
blood_researches = read_csv_file('blood_researches.csv', columns_to_extract=[2, 3, 4])
blood_parameters = read_csv_file('blood_parameters.csv', columns_to_extract=[2, 3, 4, 5])




#input_text = "Исследfвание уровня антител IgG к аллергfну с175 Норфлоксацин в крови"
#corrected_text = correct_text(input_text, all_dictionaries)
#print(corrected_text)

