import time,pickle

from selenium import webdriver
from selenium.webdriver.common.by import By


# initialize the driver
driver = webdriver.Chrome()
#add a log message after this  line
print("=== LOG: "+"chrome driver created")


# open some url
driver.get('https://online.tirupatibalaji.ap.gov.in')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https://online.tirupatibalaji.ap.gov.in/slot-booking?flow=sed&flowIdentifier=sed')
#add a log message after this  line
print("=== LOG: "+"cookies loaded and page opened ")

time.sleep(60)
try:
    while True:
        # find the refresh button by its class name and click it
        refresh_button = driver.find_element(By.CLASS_NAME, 'SlotBooking_refreshSlotsButton__1yVZz')
        # get the page source before the click
        before_click_source = driver.page_source
        refresh_button.click()
        #add a log message after this  line with readable time
        print("=== LOG: "+"refresh button clicked   "+time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(20)
        # get the page source after the click
        after_click_source = driver.page_source

        if before_click_source != after_click_source:
            print("------ The page has changed")

        time.sleep(10)

except Exception as e:
    print("An error occurred: ", str(e))




# execute JavaScript to get all unique tag names and class names
tag_names = driver.execute_script('return [...new Set([...document.querySelectorAll("*")].map(el => el.tagName))];')
class_names = driver.execute_script('return [...new Set([...document.querySelectorAll("*")].map(el => el.className))];')
#add a log message after this  line
print("=== LOG: "+"tag names and class names retrieved")

# print the results
print("Tag names:", tag_names)
print("Class names:", class_names)


cookies = driver.get_cookies()
pickle.dump(cookies, open("cookies.pkl", "wb"))
#add a log message after this  line
print("=== LOG: "+"cookies saved")

# close the driver
driver.quit()
