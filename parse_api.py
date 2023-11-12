import requests
import json
import pandas as pd
from websearch import url_to_xml

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

    for i in list_of_info:
        string = i #this is the headers that I need
        num_of_start = len(string) #length of header to get end of string
        start_idx = data.find(string) #find header
        end_idx = data.find("</Field>", start_idx) 
        lst_info.append(data[start_idx + num_of_start:end_idx])

    df = pd.DataFrame(columns=['Characteristics', 'Info'])
    df['Characteristics'] = list_of_info
    df['Info'] = lst_info
    return df

#first_url = url_to_xml('https://www.clinicaltrials.gov/study/NCT02365727?cond=Exparel&rank=1')
#test_df = xml_to_df(first_url)
#print(test_df)
#print(first_url)
