import requests
from bs4 import BeautifulSoup
import nltk
import string
import collections
import json

def parse_page_text(page):
    document = BeautifulSoup(page.text, 'html.parser')
    text = ''
    for i in document.find_all('p', recursive=True):
        text += i.get_text() + ' '
    return text

def get_stemms(page_text):
    tokens = nltk.word_tokenize(page_text)                                #Tokenize words
    tokens = [i for i in tokens if (i not in string.punctuation)]         #Clean punctuation

    stop_words = nltk.corpus.stopwords.words('english')                   #The list of common words
    tokens = [i for i in tokens if ( i not in stop_words )]               #Clean common words 'as', 'the', etc

    stemms = [i.lower() for i in stemms_generator(tokens)]
    return stemms

def stemms_generator(tokens):
    stemmer = nltk.stem.SnowballStemmer("english")                        #Create stemmer
    for t in tokens:
        yield stemmer.stem(t)

def top_20(stemms):
    stemms = collections.Counter(stemms)
    stemms = sorted([(v, k) for (k, v) in stemms.items()], reverse=True)  #reverse (k, v) and sort

    elem_counter = 1
    prev_k = None
    top_list = []                                                         #All entities

    for st in stemms:
        (k, v) = st
        if k != prev_k:
            tmp_top_list = {'rank': 0, 'count': 0, 'words': []}           #One entity
            top_list.append(tmp_top_list)
            tmp_top_list['rank']  = elem_counter
            tmp_top_list['count'] = k
            tmp_top_list['words'] = []
            elem_counter += 1
            prev_k = k
        if elem_counter > 21:
            break
        tmp_top_list['words'].append(v)

    return top_list

def export_to_json(file_path, stemms):
    with open(file_path, 'w') as outfile:
        json.dump(stemms, outfile, indent=4)

url = 'https://www.tutorialspoint.com/sambo/sambo_rules.htm'
page = requests.get(url)
page_text = parse_page_text(page)
stemms = get_stemms(page_text)
popular_stemms = top_20(stemms)
file_path = 'top_page_words/output/top20.json'
export_to_json(file_path, popular_stemms)
print('Task completed succesfully, you can find json file with top 20 words in a file', file_path)