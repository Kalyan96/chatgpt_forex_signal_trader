import sys
import time,pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time
import re
import itertools
import json
import logging



from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Specify the path to the user data directory
user_data_dir = "selenium_data"

# Specify the path to the extension CRX file
extension_path = "selenium_data\\extensions"

# Initialize ChromeOptions
chrome_options = Options()

# Add user data directory and extension
# chrome_options.add_argument("--user-data-dir=selenium_data")
chrome_options.add_argument("--user-data-dir=C:\\Users\\Kalyan\\PycharmProjects\\mt4datatest\\selenium_data")

# chrome_options.add_extension(extension_path)


# # initialize the driver
# chrome_options = Options()
# chrome_options.add_argument("--headless")# this will not open a new window and prevent distraction
driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)

#add a log message after this  line
print("=== LOG: "+"chrome driver created")

def get_source():
    return str(driver.page_source)

#### This part is used for testing to find the correct regex pattern for the website ---
test_url = "https://www.linkedin.com/jobs/search/?keywords=Engineer&location=United+States&locationId=&geoId=103644278&f_TPR=r86400&f_C=1070&f_JT=F"

# test_pattern='>(.*?) Jobs in United States.*?</t|<a class="base-card__full-link absolute(?:.|\n)*?sr-only">.*?([a-z.]+).*?<'
# test_pattern1 = '>(.*?) Jobs in United States.*?</t'
test_pattern='>([0-9]+)\s(?:[A-Za-z]+\s)+\((?:[A-Za-z0-9]+(?: [A-Za-z0-9]+)+)\)</t'


# test_pattern='"https://boards.greenhouse.(.*?)"'
if test_url :
    driver.get(test_url)
    print("=== LOG: " + "opened url")
    time.sleep(30)
    source_page = get_source()
    print(source_page)
    all_matches = re.findall(test_pattern, source_page)
    print(all_matches)
    print(len(all_matches))
    # sys.exit(1)
####  ---


# # Save cookies to a file
# cookies = driver.get_cookies()
# with open('cookies.txt', 'w') as file:
#     file.write(str(cookies))
#
# # Save extension state
# extension_file = driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": "chrome.settingsPrivate.writeExtensionFile('state.json', JSON.stringify(chrome.runtime.getManifest()));"
# })

# Close the browser
driver.quit()