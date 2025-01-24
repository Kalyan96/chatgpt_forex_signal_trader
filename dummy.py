# read a sheet using xlwings
import time
import threading

import xlwings as xw

import requests
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
import csv
import sys

#cookie handlin via selenium
from selenium import webdriver
import os

# chromedriver_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
# print("path check "+ str(os.path.exists(chromedriver_path)) )

with open("selenium_gen_cookie.txt", "r") as cookies_file:
    cookies = cookies_file.read()

driver = webdriver.Chrome()  # replace with the path to your chromedriver executable
driver.get('https://bard.google.com')


# Add each cookie to the browser session
for line in cookies.splitlines():
    if not line.startswith('#') and not line.strip() == '':
        domain, _, path, secure, expiry, name, value = line.strip().split('\t')
        secure = secure == 'TRUE'
        domain = domain.lstrip('.')
        cookie = {'domain': domain, 'path': path, 'name': name, 'value': value, 'secure': secure}
        print(cookie)
        if expiry != '0':
            cookie['expiry'] = int(expiry)

        driver.add_cookie(cookie)

#refresh the page
driver.get('https://bard.google.com')

time.sleep(60)

# Get all cookies from selenium webdriver
cookies = driver.get_cookies()
token = ''
tokencc = ''
tokents = ''

for cookie in cookies:
    if cookie['name'] == '__Secure-1PSID':
        print(cookie)
        token = cookie['value']
        print("__Secure-1PSID = " + token)
    elif cookie['name'] == '__Secure-1PSIDCC':
        print(cookie)
        tokencc = cookie['value']
        print("__Secure-1PSIDCC = " + tokencc)
    elif cookie['name'] == '__Secure-1PSIDTS':
        print(cookie)
        tokents = cookie['value']
        print("__Secure-1PSIDTS = " + tokents)



# token = "YgjNQdqM-QDR8sV_TdFPf1qW7Yysyi-JZTG6IB5NX9QlgyYXIII1lUIxmNKLO_-6vTQYMw."
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", token)
session.cookies.set("__Secure-1PSIDCC", tokencc)
session.cookies.set("__Secure-1PSIDTS", tokents)

bard = Bard(token=token, session=session)
# print(bard.get_answer("hi, could you analyse the following content?")['content'])


# sys.exit(0)




wb = xw.Book(r"D:\networks shared drive\mt4-excel-files\openpy_tester1.xlsx")
sht = wb.sheets['Sheet1']
#print the complete sheet
num_col = 27
num_row = 24
print(num_col, num_row)

# collect data
all_values = sht.range((1,1),(num_row,num_col)).value
# print(all_values)
all_values.pop(0)

#convert 2d array into csv
csv_values = ""
for row in all_values:
    # if type(row) == 'float':
    #     row=str(row)
    # print(row)
    csv_values += ','.join(str(item) if item is not None else ' ' for item in row) + '\n'
print(csv_values)


#clearing the past chat data
clr_string= "clear all data until now, start afresh "
bard.get_answer(str(clr_string))['content']
print(bard.get_answer(csv_values)['content'])

# print(bard.get_answer("what do you understand from the column headers of the data located in the 2nd row? the timeframe for each column header is located in the cell above. describe all the column headers including their timeframes and their meaning")['content'],'\n----------------Qend-----------------\n')
bard_response = ""
while True:
    user_input = input("> :  ")
    # user_input = "whats the news on all the indexes"
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    # elif user_input.lower() == 'refresh':
    else:
        bard_response = bard.get_answer(str(user_input))['content']
        print(bard_response,'\n----------------Qend-----------------\n')
        if "Response Error:" in bard_response:
            driver.get('https://bard.google.com')
            cookies = driver.get_cookies()
            # rewrite the cookie file to save the cookies
            with open('selenium_gen_cookie.txt', 'w') as file:
                # Iterate over each cookie
                for cookie in cookies:
                    # Write each cookie in the Netscape HTTP Cookie File format
                    file.write(f"{cookie['domain']}\t"
                               f"{'TRUE' if cookie['secure'] else 'FALSE'}\t"
                               f"{cookie['path']}\t"
                               f"{'TRUE' if 'expiry' in cookie else 'FALSE'}\t"
                               f"{str(int(cookie['expiry'])) if 'expiry' in cookie else ''}\t"
                               f"{cookie['name']}\t"
                               f"{cookie['value']}\n")
            for cookie in cookies:
                if cookie['name'] == '__Secure-1PSID':
                    print(cookie)
                    token = cookie['value']
                    print("__Secure-1PSID = " + token)
                elif cookie['name'] == '__Secure-1PSIDCC':
                    print(cookie)
                    tokencc = cookie['value']
                    print("__Secure-1PSIDCC = " + tokencc)
                elif cookie['name'] == '__Secure-1PSIDTS':
                    print(cookie)
                    tokents = cookie['value']
                    print("__Secure-1PSIDTS = " + tokents)
            session = requests.Session()
            session.headers = SESSION_HEADERS
            session.cookies.set("__Secure-1PSID", token)
            session.cookies.set("__Secure-1PSIDCC", tokencc)
            session.cookies.set("__Secure-1PSIDTS", tokents)

            bard = Bard(token=token, session=session)
            print("got error response from Bard, session refreshed !")
    time.sleep(10)



driver.quit()


# print(bard.get_answer("")['content'],'\n----------------Qend-----------------\n')

# print('Q2\n',bard.get_answer("what do you predict the price movement of EURUSD currency pair based on the data and also provide me your detailed reasoning for the same?")['content'])


# for row in all_values:
#     print(row)

# if the value of any cell changes, reprint teh sheet
# sht.on_change('A1', lambda: print(sht.range('A1').value)) # gives error : AttributeError: 'Sheet' object has no attribute 'on_change'