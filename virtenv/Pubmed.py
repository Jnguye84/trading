#NOT NEEDED
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

options = Options()
options.headless = True
#press enter after

lst_urls = []

for i in range (1, page_cnt):
    url = 'https://clinicaltrials.gov/search?intr=' + drug + '&aggFilters=results:with&limit=100&page=' + f'{i}' + '&tab=results'
    lst_urls.append(url)


    #soup.body.find('div _ngcontent-ng-c4179008994', attrs={'class': 'group-title'})
    #print(soup.find('span', class_='cell-value').get_text())

   #Affected/AT Risk Serious Adverse
    #<span _ngcontent-ng-c4179008994="" class="cell-value"> </span>
    #Other adverse effects
    #<span _ngcontent-ng-c4179008994="" class="cell-value">0/13 (0.00%)</span>

    #Collaborators
    #<div _ngcontent-ng-c1084249497="" class="contact-funding-item-text line-height-mono-4">No information provided</div>

    #Company/Sponsor of Study
    #<div _ngcontent-ng-c1084249497="" class="contact-funding-sponsor">Pacira Pharmaceuticals, Inc</div>