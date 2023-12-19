from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True

url = 'https://clinicaltrials.gov/search?intr=Exparel&aggFilters=results:with&limit=100&page=1'

driver = webdriver.FireFox(options=options)
driver.get(url)

# Find all button elements on the page
buttons = driver.

# Extract href links from these buttons
button_links = [button.get_attribute('href') for button in buttons if button.get_attribute('href')]

print(button_links)


driver.quit()