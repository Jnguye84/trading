# gets a list of biotech company names 
import yfinance as yf
import time
import os
import pandas as pd
#prints the company's longname
def get_collabs(ticker):
    def get_company_name(ticker):
        try:
            company = yf.Ticker(ticker)
            company_info = company.info
            if 'longName' in company_info:
                return company_info['longName']
            else:
                return None  # Handle cases where the information is unavailable
        except Exception as e:
            print(f"Error occurred: {e}")
            exit()

    # takes company's longname and downloads the 10-Q temp. Should also delete after function is done running
    entity_name = get_company_name(ticker)
    def get_10Q(name):
        # Open the company idx file
        if name is None:
            print("name Error")
            exit()
        Companyname = name.split()[0].strip(',')
        index_file = open("/Users/manas/Documents/GitHub/trading/virtenv/Financial analysis/company.idx").readlines()
        find_list = []
        item = 0
        line = 0
        try:
            while item < 1:
                i = index_file[line]
                if i.find(Companyname) != -1:
                    # print(i)
                    loc1 = i.find('10-Q')
                    loc2 = i.find("NT 10-Q") 
                    loc3 = i.find("10-Q/A")

                    #We strictly keep 10-K files, not NT 10-K or 10-K/A
                    if (loc2 == -1) and (loc1 != -1) and (loc3 == -1):
                        find_list.append(i)
                    item +=1
                    line += 1
                else:
                    # print("no")
                    line+=1
        except IndexError:
            return None


        # We will keep the information from this line in a list called find_list


        # The commands below will split the line, and send the links to a list called ReportList, and the CIK+date issued to a list called
        # Company_No (this will be  the names of our files when we download them)
        ReportList = []
        Company_No = []
        filename = None
        for i in find_list:
            split_i = i.split()
            ReportList.append("https://www.sec.gov/Archives/" + split_i[-1])
            Company_No.append(split_i[-3] + "_" + split_i[-2])
        # print(ReportList)
        # print(Company_No)

        #saving File
        import os
        os.chdir("/Users/manas/Documents/GitHub/trading/virtenv/Financial analysis/SNG data")

        def createfile(filename, content):
            name= filename + ".txt"  # Here we define the name of the file
            with open(name, "w") as file:
                file.write(str(content)) # Here we define its content, which will be the textual content from the 10-K files.
                file.close()
                print("Succeed!")

        #downloads 10-k files here
        import requests
        company_order = 0
        unable_request = 0

        for a_index in range(len(ReportList)):
            web_add = ReportList[a_index]
            filename = Companyname #Company_No[a_index]

            webpage_response = requests.get(web_add, headers={'User-Agent': 'Mozilla/5.0'}) 
            # It is very important to use the header, otherwise the SEC will block the requests after the first 5.

            if webpage_response.status_code == 200: 
                # The HTTP 200 OK success status response code indicates that the request has succeeded. 
                body = webpage_response.content
                createfile(filename, body)
            else:
                print ("Unable to get response with Code : %d " % (webpage_response.status_code))
                unable_request += 1

            a_index +=1

        print(unable_request) # Check to see if any of the downloads failed
        return filename
    
    # print(get_10Q("AbbVie"))
    stock_tenQ_name = get_10Q(entity_name)
    #searches the 10-Q for collaborators 
    
    time.sleep(1) #to allow download and indexing

    def find_collab(tenQ_Name):
        if tenQ_Name is None:
            return None
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

        text_initial = read_txt("/Users/manas/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/" + str(tenQ_Name) + ".txt")

        # print(text_initial[:30])
        text_10q = textual_content(text_initial)

        import re
        import spacy
        nlp = spacy.load("en_core_web_sm")
        from nltk.tokenize import sent_tokenize
        from fuzzywuzzy import fuzz
        target = "collaboration agreement"
        
        # Remove XML tags using regex
        clean_data = re.sub(r'<[^>]+>', '', text_10q)
        clean_data = sent_tokenize(clean_data)
        companies_mentioned = set()
        # print(clean_data)
        for item in clean_data:
            ratio = fuzz.partial_ratio(target, item)
            if 50 <= ratio <= 90:
                doc = nlp(item)
                for ent in doc.ents:
                    if ent.label_ == 'ORG':  # Check for organization entities
                        companies_mentioned.add(ent.text)
        # print(text_10q)
        os.remove("/Users/manas/Documents/GitHub/trading/virtenv/Financial analysis/SNG data/" + str(tenQ_Name) + ".txt")
        return companies_mentioned
        
    # print(stock_tenQ_name)
    # print(find_collab(stock_tenQ_name))
    return find_collab(stock_tenQ_name)

# print(get_collabs("PCRX"))

import pandas as pd
import csv
def main():
    df = pd.read_csv("virtenv/biotechTemp.csv")
    stocks = df['ticker'].to_list()
    collabs = []
    for stock in stocks:
        colabs = get_collabs(stock)
        collabs.append([stock, colabs])
        print(collabs)
    
    with open('output.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(collabs)
    # transposed_dict = {k: pd.Series(v) for k, v in dict.items()}

    # df = pd.DataFrame(transposed_dict)

    # df.to_csv('output.csv', index=False)
    return collabs
main()