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
import matplotlib.pyplot as plt
nltk.download('punkt')

#must classify name and ticker 
ticker = 'CAVA'
name = 'cava'

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
    return sentiments
print(SA_on_url(urls[0]))
print()
def get_max_occurrence_ratio(dictionary):
    # Find the key with the highest occurrence
    total = sum(dictionary.values())
    result_dict = {}
    for item in dictionary.keys():
        if total != 0:
            result_dict[item] = float(dictionary[item]/total)
    return result_dict


def sa_across_urls(): #put into dataframe
    df_pca = pd.DataFrame(columns=['Positive', 'Neutral', 'Negative', 'URL'])
    count = 0
    for url in urls:
        sa = SA_on_url(url)
        sa = get_max_occurrence_ratio(sa)
        sa['URL'] = url
        print(sa)
        df_pca.loc[count] = sa
        count += 1
    return (df_pca)

print(sa_across_urls())

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
for index, row in df_pca.iterrows():
    x, y, z, label = row['Positive'], row['Neutral'], row['Negative'], row['URL']
    ax.scatter(x, y, z, label=label)

#x is values[0], y is values[1], z is values[2]

# Set labels
ax.set_xlabel('Positive')
ax.set_ylabel('Neutral')
ax.set_zlabel('Negative')

# Add legend
ax.legend()

# Show the plot
plt.show()