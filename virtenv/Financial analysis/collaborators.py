"""
should do basically the same thing as the sentiment analysis but look for things following "collaboration with"
"""

def read_txt(file_name):
    txt_file = open(file_name,"r",encoding='UTF8')                                       
    str_txt = txt_file.read()
    return str_txt

# print(read_txt('Alt Data-Driven Investing/Financial analysis/10-Q FIles/1551152_2023-11-06.txt'))

# We will use the regex module to get everything between these patterns: <DOCUMENT>\n<TYPE>10-K and </DOCUMENT>
        # Using the regex modules it quite complex, so I recommend this long video for beginners: https://www.youtube.com/watch?v=AEE9ecgLgdQ&t=1092s

import re
text_start_pattern = re.compile(r'<DOCUMENT>') 
text_end_pattern = re.compile(r'</DOCUMENT>')
type_pattern = re.compile(r'<TYPE>10-Q[^\n]+')

# Here we will define a function that will be used to extract the textual data from 10-K txt files.

def textual_content(file):
    doc_start_list = [x.start() for x in text_start_pattern.finditer(file)] #assigns the first index from the starting pattern created before
    doc_end_list = [x.end() for x in text_end_pattern.finditer(file)] #assigns the last index from the ending pattern created before
    type_list = [x[len('<TYPE>'):] for x in type_pattern.findall(file)] #assigns the type of the documents, which will always be 10-K's because we restricted it before

    for doc_type, start_index, end_index in zip(type_list, doc_start_list, doc_end_list):
        report_content = file[start_index:end_index]
        break
    return report_content

text_initial = read_txt('virtenv/Financial analysis/10-Q FIles/1551152_2023-11-06.txt')

# print(text_initial[:30])
text_10q = textual_content(text_initial)
# print(text_10q)

pattern = r'Collaboration with ([^.]+)\.'

# Search for the pattern in the XML excerpt
matches = re.findall(pattern, text_10q)

if matches:
    print("\n Companies with collaborations:")
    for company_name in matches:
        print(f"- {company_name}")
else:
    print("No collaboration found.")


