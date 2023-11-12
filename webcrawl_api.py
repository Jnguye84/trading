from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from parse_api import list_of_info, xml_to_df
from selenium.webdriver.support.ui import Select

# Set up options for a headless Firefox browser
options = Options()
options.headless = True

url = 'https://classic.clinicaltrials.gov/api/gui/demo/simple_full_study'

# Create a new instance of the Firefox WebDriver (you can use other browsers as well)
driver = webdriver.Firefox(options=options)

# Navigate to the webpage
driver.get(url)

for count in range (1,2):
    # Find the textarea element with the specified name attribute
    textarea = driver.find_element("name", "expr")
    min_rank = driver.find_element("id", "min_rnk")
    max_rank = driver.find_element("id", "max_rnk")

    # Clear the existing content in the textarea (if any)
    textarea.clear()

    # Enter the word "experal" into the textarea
    textarea.send_keys('experal')
    min_rank.send_keys(f"{count}")
    max_rank.send_keys(f"{count}")

    # Find the select element by its name, ID, or XPath, etc.
    select_element = Select(driver.find_element('name', 'fmt'))
    
    # Select an option by visible text
    select_element.select_by_visible_text('xml')

    # Find the button element by its name, ID, XPath, etc.
    button = driver.find_element('id','SendRequestButton')

    # Click the button
    button.click()

    # Find the element by its ID
    element_with_id = driver.find_element('id','APIURL')
    element_url = element_with_id.get_attribute('href')

    print(xml_to_df(element_url))


driver.quit()
