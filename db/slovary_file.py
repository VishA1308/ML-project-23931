import csv

def read_csv_file(file_path, delimiter=';', columns_to_extract=None):
    """Читает CSV файл и извлекает указанные колонки."""
    extracted_values = [[] for _ in range(len(columns_to_extract))]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader) 
        print(f"Заголовки из {file_path}: {headers}")
        
        for row in reader:
            for i, col_index in enumerate(columns_to_extract):
                if col_index < len(row):
                    extracted_values[i].append(row[col_index].strip())
                else:
                    extracted_values[i].append("")

    return [list(set(values)) for values in extracted_values]



"""
params_achive_norms = read_csv_file('params_archive_norms.csv', columns_to_extract=[2, 3, 4, 5])
params_achive_names = read_csv_file('params_archive_names.csv', columns_to_extract=[2, 3, 4])
genetics_parameters = read_csv_file('genetics_parameters.csv', columns_to_extract=[2, 3, 4, 5])
genetics_researches = read_csv_file('genetics_researches.csv', columns_to_extract=[2, 3, 4])
"""
"""
print("Архив норм:")
print("Исследования:", params_achive_norms[0])
print("Параметры:", params_achive_norms[1])
print("Нормы:", params_achive_norms[2])
print("Единицы измерения:", params_achive_norms[3])

print("\nАрхив названий:")
print("Исследования:", params_achive_names[0])
print("Параметры:", params_achive_names[1])
print("Иностранные названия:", params_achive_names[2])

print("\nГенетические параметры:")
print("Исследования:", genetics_parameters[0])
print("Параметры:", genetics_parameters[1])
print("Нормы:", genetics_parameters[2])
print("Единицы измерения:", genetics_parameters[3])

print("\nГенетические исследования:")
print("Исследования:", genetics_researches[0])
print("Альтернативные названия:", genetics_researches[1])
print("Иностранные названия:", genetics_researches[2])
"""
