import requests
import json
import html_to_json
import pandas as pd

url = 'https://classic.clinicaltrials.gov/api/query/full_studies?expr=experal&min_rnk=1&max_rnk=1&fmt=xml'
response = requests.get(url)
data = response.text

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

lst_info = []

for i in list_of_info:
    string = i #this is the headers that I need
    num_of_start = len(string)
    start_idx = data.find(string)
    end_idx = data.find("</Field>", start_idx)
    lst_info.append(data[start_idx + num_of_start:end_idx])

df = pd.DataFrame(columns=['Characteristics', 'Info'])
df['Characteristics'] = list_of_info
df['Info'] = lst_info

print(df)