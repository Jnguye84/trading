from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class WebCrawl():
    def Get_Links(self):

        driver = webdriver.Chrome()

        # Navigate to the website
        driver.get("https://www.clinicaltrials.gov/")

        # Find the search box element by ID
        search_box = driver.find_element("id", "advcond")


        # Input a search term
        search_box.send_keys("Exparel")

        search_box.send_keys(Keys.RETURN)

        # Allow some time for the search results to load (adjust as needed)
        time.sleep(2)

        # Extract links from the search results
        links = driver.find_elements("xpath",'//a[@href]')
        lst_of_links = []
        # Print the links or store them in a list for further processing
        for link in links:
            href = link.get_attribute('href')
            lst_of_links.append(href)
        # Close the browser
        driver.quit()
        self.lst_of_links = lst_of_links
        filtered_list = [s for s in lst_of_links if 'NCT' in s]
        self.filtered_list = filtered_list

obj = WebCrawl()
obj.Get_Links()
print(obj.filtered_list)

