from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from bert import sentiment
# nltk.download('punkt')

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
    
# Set the User-Agent header to mimic a web browser
req = Request(
    url='https://www.zacks.com/stock/news/2177620/pacira-pcrx-q3-earnings-and-revenues-miss-23-view-updated', #this is where the variable needs to go
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read()
article_str = text_from_html(webpage) #string from the entire webpage
# print(article_str)
from nltk.tokenize import sent_tokenize


sentences = sent_tokenize(article_str)
# print(sentences)
# print(sentiment(sentences))
for sentence in sentences:
    if len(sentence)< 512:
        temp = sentiment(sentence)
        if temp[0]['label'] == 'Positive':
            print(sentence,'\n')

