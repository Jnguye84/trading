from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from webcrawl_api import lst
import pandas as pd
# nltk.download('punkt')

def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

list_of_info = [
    'OrgFullName',
    "OfficialTitle", #title of study
    "StatusVerifiedDate",
    "OverallStatus",
    "StartDate",
    "CompletionDate",
    "BriefSummary",
    "Condition",
    "ArmGroupDescription",
    "ArmGroupInterventionName", #drug
    "PrimaryOutcomeDescription",
    "SecondaryOutcomeDescription",
    "OtherOutcomeMeasure",
    "OtherOutcomeDescription",
    "OtherOutcomeTimeFrame",
    "OtherOutcomeDescription", #length of stay
    "EligibilityCriteria", #participants
    "FlowGroupDescription",
    "FlowGroupDescription",
    "OutcomeMeasureTitle",
    "OutcomeMeasureDescription",
    "OutcomeMeasureTimeFrame",
    "OutcomeGroupDescription",
    "OutcomeMeasureDescription",
    "OutcomeMeasureTimeFrame",
]

def xml_to_df(data):
    lst_info = []

    req = Request(
        url=data, #this is where the variable needs to go
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    webpage = urlopen(req).read()
    webpage = webpage.decode('utf-8')

    for i in list_of_info:
        string = i #this is the headers that I need
        num_of_start = len(string) #length of header to get end of string
        start_idx = webpage.find(string) #find header
        end_idx = webpage.find("</Field>", start_idx) 
        lst_info.append(webpage[start_idx + num_of_start:end_idx])

    df = pd.DataFrame(columns=['Characteristics', 'Info'])
    df['Characteristics'] = list_of_info
    df['Info'] = lst_info
    return df

for i in lst:
    print(xml_to_df(i))


#from nltk.tokenize import sent_tokenize


#sentences = sent_tokenize(article_str)
# print(sentences)
# print(sentiment(sentences))
#for sentence in sentences:
    #if len(sentence)< 512:
        #temp = sentiment(sentence)
        #if temp[0]['label'] == 'Positive':
            #print(sentence,'\n')

