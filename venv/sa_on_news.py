#finding SA for first 50 articles in alpha vantage API based on ticker
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from bert import sentiment
import requests
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import pandas as pd
nltk.download('punkt')

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

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers' +ticker + '&apikey=NUITBAL6RYNHAL6G'
r = requests.get(url)
data = r.json()
urls = []

for i in range(len(data['feed'])):
    obj = data['feed'][i]
    urls.append(obj['url'])

def SA_on_url(url_given):
    sentiments = {'Positive' : 0, 'Neutral' : 0, 'Negative': 0}
    req = Request(
    url=str(url_given), #this is where the variable needs to go
    headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    article_str = text_from_html(webpage) #string from the entire webpage

    sentences = sent_tokenize(article_str)
    for sentence in sentences:
        words = word_tokenize(sentence)
        if len(sentence)< 512 and (ticker in words or name in words):
            temp = sentiment(sentence)
            temp_label = temp[0]['label']
            sentiments[temp_label] += 1
    total = 0
    for i in sentiments.values(): total = total + i
    for i in sentiments.keys(): sentiments[i] = sentiments[i]/total
    return sentiments

def sa_across_urls(): #put into dataframe
    df_pca = pd.DataFrame(columns=['Positive', 'Neutral', 'Negative', 'URL'])
    count = 0
    for url in urls:
        sa = SA_on_url(url)
        sa['URL'] = url
        df_pca.loc[count] = sa
        count += 1
    return (df_pca)

#print(sa_across_urls())

