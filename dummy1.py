import sys
import time

from selenium import webdriver
import os

# chromedriver_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
# print("path check "+ str(os.path.exists(chromedriver_path)) )

with open("cookie.txt", "r") as cookies_file:
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
driver.get('https://bard.google.com')  # replace with the URL you're interested in

# Get all cookies from selenium webdriver
cookies = driver.get_cookies()
token = ''
tokencc = ''
tokents = ''

for cookie in cookies:
    if cookie['name'] == '__Secure-1PSID':
        print(cookie)
        token = cookie['value']
    elif cookie['name'] == '__Secure-1PSIDCC':
        print(cookie)
        tokencc = cookie['value']
    elif cookie['name'] == '__Secure-1PSIDTS':
        print(cookie)
        tokents = cookie['value']


# Open the file to save the cookies
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

driver.quit()


sys.exit(0)



import requests
import browsercookie
cj = browsercookie.chrome()
r = requests.get('https://bard.google.com/', cookies=cj)
print(r.text)


from bardapi import Bard

bard = Bard(token_from_browser=True)
res = bard.get_answer("Do you like cookies?")
print(res)