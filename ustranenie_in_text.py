import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


def filter_text(text: str) -> str:
  
    # Удаляем все символы, кроме букв русского алфавита и цифр
    text = re.sub(r'[^а-яА-ЯёЁ0-9s]', ' ', text)
    words = word_tokenize(text, language='russian')
    
    stop_words = set(stopwords.words('russian'))
    
    # Фильтруем слова, исключая стоп-слова
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

'''
# Пример использования функции
text = "Это пример текста 1204 @@@ 4 4u, в котором есть слова, не имеющие смысла."
filtered_result = filter_text(text)
print(filtered_result)
'''