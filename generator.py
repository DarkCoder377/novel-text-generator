import re
import requests
import random
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

url = input("please input your url to your text source: ")


response = requests.get(url)


if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')


    extracted_text = []

    for paragraph in paragraphs:
        text = paragraph.get_text()
        extracted_text.append(text)


    output_file = 'extracted text.txt'

    with open(output_file, 'w', encoding='utf-8') as file:
        for text in extracted_text:
            file.write(text + '\n')
else:
    print('Failed to retrieve the web page. Status code:', response.status_code)

with open(output_file, 'r', encoding='utf-8') as file:
    text = file.read()

text = text.lower()


words = word_tokenize(text)


stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]


filtered_words = [word for word in filtered_words if word.isalnum()]

output_file1 = 'extracted text preprocessed.txt'

with open(output_file1, 'w', encoding='utf-8') as file:
        for word in filtered_words:
            file.write(word + '\n')



with open(output_file1, 'r', encoding='utf-8') as file:
    input_text = file.read()


words = input_text.split()

def build_markov_model(words):
    markov_model = {}
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        if current_word in markov_model:
            markov_model[current_word].append(next_word)
        else:
            markov_model[current_word] = [next_word]
    return markov_model


def generate_text(markov_model, length=10, seed=None):
    if seed is None:
        seed = random.choice(list(markov_model.keys()))
    
    generated_text = [seed]
    
    for _ in range(length):
        next_word = random.choice(markov_model[seed])
        generated_text.append(next_word)
        seed = next_word
    
    return ' '.join(generated_text)

markov_model = build_markov_model(words)

generated_text = generate_text(markov_model, length=20)

output_file3 = 'generated text.txt'

with open(output_file3, 'w', encoding='utf-8') as file:
    file.write(generated_text)

print("Files are generated.")

input("Press Enter to quit")