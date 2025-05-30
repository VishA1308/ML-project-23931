# Проект "Распознавание результатов анализов"

[Демо-версия сайта](https://visha1308.github.io/ML-project-23931/)

Куратор - Бондаренко Денис

Участники: Басова Юлия, Вишнякова Алиса, Жильцова Марина

Задачи проекта:

1. Предобработка изображений: Нормализация изображений: изменение яркости, контраста,
устранение шумов.

2. Распознавание текста (+ выравнивание)
- Использование OCR для извлечения текста с изображений (пример либы: Tesseract)
- Постобработка текста: исправление ошибок OCR, удаление лишних символов, разделение текста
на строки и столбцы.

3. Извлечение данных:

Анализ текста для выделения ключевых элементов:
- Название показателя (например, "Глюкоза", "Холестерин").
- Значение показателя (например, "5.2", "120").
- Единица измерения (например, "ммоль/л", "мг/дл").
- Дата сдачи анализа
- Название клиники

4. Доработки:
- Учет вариативности в наименованиях показателей
- Разнообразие единиц измерения (Один и тот же показатель может быть выражен в различных
единицах измерения, что требует дополнительной обработки для приведения данных к единому
стандарту)
- Результаты анализов могут быть представлены в рукописном виде или в форматах, которые не
соответствуют стандартной структуре

## Branch project
Наиболее полная версия проекта

### benchmark
Код и файлы для тестирования и оценки решений и инструментов
### db
Таблицы на основе медицинских справочников с названиями анализов и нормами значений
### res
Обработанные изображения
### templates
Тестовые изображения
### T9.py
Обработка опечаток
### extraction.py
Извлечение данных из текста (названия, показатели и т.д.)
### jiwer_test.py
Вычисление метрик WER, CER, MER (библиотека jiwer)
### main.py
Основной исполняемый файл
### preprocess_of_image.py
Обработка изображений (устранение шумов, коррекция контрастности, яркости)
### tesseract_test.py
Применение pytesseract для извлечения текста
### ustranenie_in_text.py
Удаление мусорных символв из текста

## Branch app
Версия для Docker

## Branch demo
Устаревшая версия

## Branch doc
Версия с структурой и диаграммами

## Branch gh-pages
Ветка для GitHub Pages

## Branch tesseract_learning
Файлы для дообучения Tesseract OCR

## Branch web_src
Source-файлы сайта
