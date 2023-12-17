# Open the company idx file
index_file = open("Alt Data-Driven Investing/Financial analysis/company.idx").readlines()
find_list = []
item = 0
line = 0

while item < 1:
    i = index_file[line]
    if i.find("AbbVie") != -1:
        print(i)
        loc1 = i.find('10-Q')
        loc2 = i.find("NT 10-Q") 
        loc3 = i.find("10-Q/A")

        #We strictly keep 10-K files, not NT 10-K or 10-K/A
        if (loc2 == -1) and (loc1 != -1) and (loc3 == -1):
            find_list.append(i)
        item +=1
        line += 1
    else:
        print("no")
        line+=1


# We will keep the information from this line in a list called find_list


# The commands below will split the line, and send the links to a list called ReportList, and the CIK+date issued to a list called
# Company_No (this will be  the names of our files when we download them)
ReportList = []
Company_No = []
for i in find_list:
    split_i = i.split()
    ReportList.append("https://www.sec.gov/Archives/" + split_i[-1])
    Company_No.append(split_i[-3] + "_" + split_i[-2])
print(ReportList)
print(Company_No)

#saving File
import os
os.chdir("/workspaces/projects/Alt Data-Driven Investing/Financial analysis/10-Q FIles")

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
    filename = Company_No[a_index]

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