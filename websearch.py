from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen

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
    url='https://www.prnewswire.com/news-releases/arcellx-announces-partial-clinical-hold-lifted-on-immagine-1-phase-2-clinical-program-and-reports-second-quarter-financial-results-301900055.html', #this is where the variable needs to go
    headers={'User-Agent': 'Mozilla/5.0'}
)
webpage = urlopen(req).read()
article_str = text_from_html(webpage) #string from the entire webpage
print(article_str)