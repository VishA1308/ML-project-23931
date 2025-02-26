import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


#text = "Это пример текс""та 1204 "" @@@  4 4u, в котором есть слова, не имеющие смысла."
text = re.sub(r'[^а-яА-ЯёЁ0-9s]', ' ', text)


words = word_tokenize(text, language='russian')

stop_words = set(stopwords.words('russian'))
#print(stop_words)


filtered_words = [word for word in words if word.lower() not in stop_words]

# Результат
filtered_text = ' '.join(filtered_words)
print(filtered_text)
