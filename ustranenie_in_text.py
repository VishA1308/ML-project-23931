import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


with open('text.txt', 'r') as fin:
    text = fin.readlines()
    text = ' '.join(text)

text = re.sub(r'[^а-яА-ЯёЁ0-9s]', ' ', text)


words = word_tokenize(text, language='russian')

stop_words = set(stopwords.words('russian'))
#print(stop_words)


filtered_words = [word for word in words if word.lower() not in stop_words]

# Результат
filtered_text = ' '.join(filtered_words)
print(filtered_text)
