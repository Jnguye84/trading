from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ClinicalTrialsInfo:
    def __init__(self, url):
        self.url = url
        self.adverse_events = None
        self.collaborators = None

    def get_adverse_events(self):
        driver = webdriver.Chrome()  # You can change this according to your WebDriver

        try:
            driver.get(self.url)
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "adverse-events"))
            )

            element_list = element.text.split("\n")
            element_list = element_list[element_list.index('Serious Adverse Events'):]
            totals = []
            totals_indices = []
            for index, item in enumerate(element_list):
                if "Total" in item.split(" "):
                    totals.append(item)
                    totals_indices.append(index)
            for index, item in enumerate(element_list):
                if index > max(totals_indices) and "%" in list(item):
                    totals.append(item)

            self.adverse_events = totals

        finally:
            driver.quit()

    def get_collaborators(self):
        driver = webdriver.Chrome()  # You can change this according to your WebDriver

        try:
            driver.get(self.url)
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "collaborators-and-investigators"))
            )
            element_list = element.text.split("\n")
            colab_indices = [element_list.index("Sponsor"), element_list.index("Collaborators"),
                             element_list.index("Investigators")]
            colabs = []
            for item in colab_indices:
                colabs.append(element_list[item + 1])

            self.collaborators = colabs

        finally:
            driver.quit()


# Usage:
url = "https://clinicaltrials.gov/study/NCT02199574?intr=Exparel&aggFilters=results:with&rank=1&tab=results"
trial_info = ClinicalTrialsInfo(url)
trial_info.get_adverse_events()
trial_info.get_collaborators()

print("Adverse Events:", trial_info.adverse_events)
print("Collaborators:", trial_info.collaborators)
