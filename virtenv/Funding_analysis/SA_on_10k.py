
def read_txt(file_name):
    txt_file = open(file_name,"r",encoding='UTF8')                                       
    str_txt = txt_file.read()
    return str_txt

# print(read_txt('/Users/manas/Documents/GitHub/trading/virtenv/Funding_analysis/10kFiles/6955_2023-10-20.txt'))

# We will use the regex module to get everything between these patterns: <DOCUMENT>\n<TYPE>10-K and </DOCUMENT>
        # Using the regex modules it quite complex, so I recommend this long video for beginners: https://www.youtube.com/watch?v=AEE9ecgLgdQ&t=1092s

import re
text_start_pattern = re.compile(r'<DOCUMENT>') 
text_end_pattern = re.compile(r'</DOCUMENT>')
type_pattern = re.compile(r'<TYPE>10-K[^\n]+')

# Here we will define a function that will be used to extract the textual data from 10-K txt files.

def textual_content(file):
    doc_start_list = [x.start() for x in text_start_pattern.finditer(file)] #assigns the first index from the starting pattern created before
    doc_end_list = [x.end() for x in text_end_pattern.finditer(file)] #assigns the last index from the ending pattern created before
    type_list = [x[len('<TYPE>'):] for x in type_pattern.findall(file)] #assigns the type of the documents, which will always be 10-K's because we restricted it before

    for doc_type, start_index, end_index in zip(type_list, doc_start_list, doc_end_list):
            report_content = file[start_index:end_index]
    return report_content

text_initial = read_txt('/Users/manas/Documents/GitHub/trading/virtenv/Funding_analysis/10kFiles/6955_2023-10-20.txt')
text_10k = textual_content(text_initial)
print(text_10k[0:30])
print(text_10k[-30:])


from bs4 import BeautifulSoup
def BeautifulSoup_clean1(str_txt):
    soup = BeautifulSoup(str_txt,'html.parser')
    return soup.get_text() # Here we return only the textual content, without the XML tags


import string
from nltk.tokenize import word_tokenize

def further_clean(text):
    # First, for each of the following characters (or symbols), the function replaces it by an empty space on the text 
    for a_sign in ['\\n', '\\t', '☐', '☒', '\xa0', '●', '“', '”']:
        text = text.replace(a_sign, " ")

    # Preserve periods used in abbreviations (e.g., U.S., Inc.)
    text = re.sub(r'([A-Za-z])\.([A-Za-z])', r'\1<prd>\2', text)

    # Here, for each punctuation in a set of all existing punctuations, the function also replaces it by an empty space.
    for a_punc in string.punctuation:
        if a_punc != '.':
            text = text.replace(a_punc, " ")

    # Replace the preserved periods with an actual period and a space
    text = text.replace('<prd>', '.')

    # Moreover, the function replaces '\s+' (which represents a sequence of empty spaces) by a single empty space, avoiding unnecessary spaces
    # and also sets all letters to lowercase to make it easier to analyze later.
    text = re.sub('\s+', " ", text).lower()

    return text.strip()


cleaned_data = further_clean(BeautifulSoup_clean1(text_10k))
from nltk.tokenize import sent_tokenize

sentences = sent_tokenize(cleaned_data)
print(len(sentences))

from bert import sentiment
def SA_on_text(sentence_list):
    sentiments = {'Positive' : 0, 'Neutral' : 0, 'Negative': 0} 
    # print(article_str

    # print(sentences)
    # print(sentiment(sentences))
    for sentence in sentence_list:
        if len(sentence)< 512:
            # print(sentence)
            temp = sentiment(sentence)
            temp_label = temp[0]['label']
            sentiments[temp_label] += 1
    return sentiments

print(SA_on_text(sentences))