import os
import requests
import re
# Open the company idx file
def find_occurences(name):
    index_file = open("Insider_buying/company.idx").readlines()
    find_list = []
    item = 0
    line = 0

    while line < len(index_file):
        i = index_file[line]
        if i.find(name) != -1:
            loc1 = i.find('13D')
            loc2 = i.find("13G") 
            loc3 = i.find("13E3")
            loc4 = i.find("13H")

            #We strictly keep 10-K files, not NT 10-K or 10-K/A
            if (loc2 != -1) or (loc1 != -1) or (loc3 != -1) or (loc4 != -1):
                find_list.append(i)
                item +=1
            line += 1
        else:
            line+=1
    return item
# print(find_occurences("SAFEGUARD"))


def find_form4(name):
    index_file = open("Insider_buying/company.idx").readlines()
    list = []
    for line in index_file:
        loc = line.find(name)
        if loc != -1:
            try:
                # print(line.split())
                if '4' in line.split():
                    list.append(line)
            except:
                pass
    return list
x = find_form4("")
print(len(x))

def get_form4s(list_of_4s,ticker=None, file_path="Insider_buying/form4s"):
    
    links = ["https://www.sec.gov/Archives/" + item.split()[-1] for item in list_of_4s]
    os.chdir(file_path)
    def createfile(filename, content):
        name= str(filename) + ".txt"  # Here we define the name of the file
        with open(name, "w") as file:
            file.write(str(content)) # Here we define its content, which will be the textual content from the 10-K files.
            file.close()
            print("Succeed!")
        return links
    unable_request = 0

    for a_index in range(len(links)):
        web_add = links[a_index]
        filename = a_index 
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

# print(get_form4s(x))


def on_4(path, ticker):
    def read_txt(file_name):
        txt_file = open(file_name,"r",encoding='UTF8')                                       
        str_txt = txt_file.read()
        return str_txt
    try:
        text = read_txt(path)
        
        pattern = r'<issuerTradingSymbol>(.*?)</issuerTradingSymbol>'
        issuer = re.findall(pattern, text, re.DOTALL)
        if issuer[0] == ticker:
            transaction_pattern = r'<transactionAcquiredDisposedCode>(.*?)</transactionAcquiredDisposedCode>'
            transaction = re.findall(transaction_pattern, text, re.DOTALL)
            value_pattern = r"<value>(.*?)</value>"
            code = re.findall(value_pattern, transaction[0], re.DOTALL)
        if issuer != ticker:
            print(issuer,path)
        return code[0]
    except:
        return None

# print(on_4("Insider_buying/form4s/0.txt","ACM"))
    
def on_all_4s (folderpath,ticker):
    codes = []
    for filename in os.listdir(folderpath):
        file_path = os.path.join(folderpath, filename)
        code = on_4(file_path, ticker)
        if code is not None:
            codes.append(code)
    return codes

print(on_all_4s("Insider_buying/form4s","ACM"))
