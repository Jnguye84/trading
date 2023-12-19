from bs4.element import Comment
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4.element import Comment
from urllib.request import Request, urlopen
import time
import csv

drug = str(input("Name the drug you'd like to find with first letter capitalized: "))
page_cnt = int(input("Name how many case studies you'd like to find: "))

options = Options()
options.headless = True
lst = []
url = 'https://classic.clinicaltrials.gov/api/gui/demo/simple_full_study'

driver = webdriver.Firefox(options=options)
driver.get(url)
driver.implicitly_wait(page_cnt + 10)

for count in range (1,page_cnt+1):
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

    time.sleep(3)
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
    "NCTId" #id to get results
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
        num_of_start = len(string) + 2 
        start_idx = webpage.find(string) 
        end_idx = webpage.find("</Field>", start_idx) 
        lst_info.append(webpage[start_idx + num_of_start:end_idx])
    return lst_info

for i in lst:
    list_ids = xml_to_df(i)

csv_file = "virtenv/my_NCTIds.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(list_ids)

drug_file = 'virtenv/drugs.csv'

with open(drug_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(drug)