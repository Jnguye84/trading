from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from bert import sentiment
import pandas as pd
import numpy as np
# nltk.download('punkt')

#must classify name and ticker 
ticker = 'CAVA'
name = 'Cava'

def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=CAVA&apikey=NUITBAL6RYNHAL6G'
r = requests.get(url)
data = r.json()
urls = []
# print(data['feed'])
for i in range(len(data['feed'])):
    obj = data['feed'][i]
    # print(obj['url'])
    urls.append(obj['url'])
# print(urls)
# print()
def SA_on_url(url_given):
    sentiments = {'Positive' : 0, 'Neutral' : 0, 'Negative': 0}
    req = Request(
    url=str(url_given), #this is where the variable needs to go
    headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    article_str = text_from_html(webpage) #string from the entire webpage
    # print(article_str)
    from nltk.tokenize import sent_tokenize, word_tokenize

    sentences = sent_tokenize(article_str)
    # print(sentences)
    # print(sentiment(sentences))
    for sentence in sentences:
        words = word_tokenize(sentence)
        if len(sentence)< 512 and (ticker in words or name in words):
            # print(sentence)
            temp = sentiment(sentence)
            temp_label = temp[0]['label']
            sentiments[temp_label] += 1
            # if temp[0]['label'] == 'Positive':
            #     print(sentence,'\n')
            # if temp[0]['label'] == 'Negative':
            #     print(sentence,'\n')
    return sentiments
print(sentiment(url[0]))
pass
def get_max_occurrence_ratio(dictionary):
    # Find the key with the highest occurrence
    total = sum(dictionary.values()) +1
    result_dict = {}
    for item in dictionary.keys():
        result_dict[item] = dictionary[item]/total

    return result_dict

def extract_num(lst):
    res = []
    for i in lst:
        i = str(i).split(',')[1]
        i = float(str(i).split(')')[0])
        res.append(i)
    return res

def sa_across_urls():
    running_total = {'Positive':0, 'Neutral':0, 'Negative':0}
    sa_1 = []
    sa_2 = []
    sa_3 = []
    df = pd.DataFrame()
    df_list_of_sources = []
    for url in urls:
        df_list_of_sources.append(url)
        sa = SA_on_url(url)
        print(sa)
        sa = get_max_occurrence_ratio(sa)
        sa_1.append(list(sa.items())[0])
        sa_2.append(list(sa.items())[1])
        sa_3.append(list(sa.items())[2])
    sa_1 = extract_num(sa_1)
    sa_2 = extract_num(sa_2)
    sa_3 = extract_num(sa_3)
    df['Positive'] = sa_1
    df['Neutral'] = sa_2
    df['Negative'] = sa_3
    return df, df_list_of_sources

df = sa_across_urls()[0]
df_list_of_sources = sa_across_urls()[1]
print(df)