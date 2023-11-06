from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import pandas as pd
import requests
import numpy as np

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

def findTextfromURL(urlstring): #press report
    # Set the User-Agent header to mimic a web browser
    req = Request(
        url=urlstring, #this is where the variable needs to go
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    article_str = text_from_html(webpage) #string from the entire webpage
    return article_str

def findTable(urlstring):
    webpage = requests.get(urlstring)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    dfs = pd.read_html(webpage.text, attrs={'class':'de-lightBorder'})
    recruitment = dfs[0]
    participantflow = dfs[1]
    baselinechar = dfs[2]
    primaryoutcome = dfs[3]
    analysispopdesc_1 = dfs[4]
    secondoutcome = dfs[5]
    analysispopdesc_2 = dfs[6]
    secondaryoutcome = dfs[7]
    outcomemeasured = dfs[8]
    adverseevents = dfs[9]

#findTable("https://classic.clinicaltrials.gov/ct2/show/results/NCT02008370?cond=exparel&draw=2&rank=1")
