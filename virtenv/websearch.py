from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
import pandas as pd
# nltk.download('punkt')
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4.element import Comment
from urllib.request import Request, urlopen
from sqlalchemy import create_engine
import time 
options = Options()
options.headless = True
lst = []
url = 'https://classic.clinicaltrials.gov/api/gui/demo/simple_full_study'

#press enter after
drug = str(input("Name the drug you'd like to find: "))
number = int(input("Name how many case studies you'd like to find: "))

driver = webdriver.Firefox(options=options)
driver.get(url)
driver.implicitly_wait(number + 10)

for count in range (1,number):
    # Find the textarea element with the specified name attribute
    textarea = driver.find_element("name", "expr")
    min_rank = driver.find_element("id", "min_rnk")
    max_rank = driver.find_element("id", "max_rnk")

    # Clear the existing content in the textarea (if any)
    textarea.clear()
    min_rank.clear()
    max_rank.clear()

    # Enter the word "experal" into the textarea
    textarea.send_keys(f'{drug}')
    min_rank.send_keys(f"{count}")
    max_rank.send_keys(f"{count}")

    # Find the select element by its name, ID, or XPath, etc.
    select_element = Select(driver.find_element('name', 'fmt'))

    select_element.select_by_visible_text('xml')

    # Find the button element by its name, ID, XPath, etc.
    button = driver.find_element('id','SendRequestButton')

    # Click the button
    button.click()

    # Find the element by its ID
    element_with_id = driver.find_element('id','APIURL')
    element_url = element_with_id.get_attribute('href')
    lst.append(element_url)

driver.quit()

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
    "PrimaryCompletionDate",
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
        url=data, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    webpage = urlopen(req).read()
    webpage = webpage.decode('utf-8')

    for i in list_of_info:
        string = i 
        num_of_start = len(string) + 1 
        start_idx = webpage.find(string) 
        end_idx = webpage.find("</Field>", start_idx) 
        lst_info.append(webpage[start_idx + num_of_start:end_idx])

    df = pd.DataFrame(columns=['Characteristics', 'Info'])
    df['Characteristics'] = list_of_info
    df['Info'] = lst_info
    return df

overall_df = pd.DataFrame()
overall_df['Characteristics'] = list_of_info

for i in lst:
    overall_df[[f'{i}']] = xml_to_df(i)['Info']
    
#overall_df.to_excel('exparel_field.xlsx')