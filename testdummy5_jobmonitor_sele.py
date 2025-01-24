import sys
import time,pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import itertools
import json
import logging
from datetime import datetime ,timedelta



from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_source():
    return str(driver.page_source)


def get_test_updates():
    class_name = "latestUpdates_list__2tn1D"
    news_list_container = driver.find_element(By.CLASS_NAME, class_name)
    # news_updates = news_list_container.find_elements(By.TAG_NAME, "li")
    print(news_list_container)
    # return ["- "+update.text+"\n" for update in news_updates]


def get_current_updates():
    class_name = "latestUpdates_list__2tn1D"
    news_list_container = driver.find_element(By.CLASS_NAME, class_name)
    news_updates = news_list_container.find_elements(By.TAG_NAME, "li")
    return ["- "+update.text+"\n" for update in news_updates]

store_file="Savefile.json"
def save_to_file(my_dict):
    with open(store_file, 'w') as file:
        json.dump(my_dict, file)

def read_from_file_dict():
    with open(store_file, 'r') as file:
        loaded_dict = json.load(file)
        return loaded_dict

def send_message(bot, message):
    global chat_id
    bot.send_message(chat_id=chat_id, text=message)

def echo(update, context):
    user_message = update.message.text
    update.message.reply_text(f'You said: {user_message}')

    # After replying, send a message
    # send_message(context.bot, update.message.chat_id, "This is an additional message.")





# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
token = '6825288199:AAEJkTAoUhSTUJEDsQx4s0HW7ghNhMn95ms'
chat_id = "6020027159"

# initialize the driver
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\Kalyan\\PycharmProjects\\mt4datatest\\selenium_data")
# chrome_options.add_argument("--headless")# this will not open a new window and prevent distraction
driver = webdriver.Chrome(options=chrome_options)


#add a log message after this  line
print("=== LOG: "+"chrome driver created")

# store_file = "testdummy3_ttdmonitor_lastupdate.txt"


# updater = Updater(bot=bot)
# dispatcher = updater.dispatcher
# dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, echo))
# updater.start_polling()
# print ("chatbot initialized")

#### This part is used for testing to find the correct regex pattern for the website ---
test_url = ""
# test_url="https://www.linkedin.com/jobs/search/?currentJobId=3765375579&f_C=407222&f_TPR=r86400&f_WT=2&geoId=103644278&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
test_pattern='"https://www.linkedin.com/jobs/view/(.*?)"'
# test_pattern='"https://boards.greenhouse.(.*?)"'
if test_url :
    driver.get(test_url)
    print("=== LOG: " + "opened url")
    time.sleep(5)
    source_page = get_source()
    print(source_page)
    all_matches = re.findall(test_pattern, source_page)
    print(all_matches)
    print(len(all_matches))
    sys.exit(1)
####  ---



# urls = ["https://careers.hpe.com/us/en/search-results?ak=urk3r534f0wz","https://careers.nokia.com/jobs/search/41116900","https://careers.juniper.net/#/","https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/requisitions?lastSelectedFacet=AttributeChar12&location=United+States&locationId=300000000149325&selectedFlexFieldsFacets=%22AttributeChar15%7COCI%7C%7CAttributeChar12%7CLess+than+10+applicants%22"]
urls = {
    "Hp":"https://careers.hpe.com/us/en/search-results?ak=urk3r534f0wz",
    "Nokia":"https://careers.nokia.com/jobs/search/41116900",
    "Juniper":"https://careers.juniper.net/#/",
    "Oracle":"https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/requisitions?lastSelectedFacet=AttributeChar12&location=United+States&locationId=300000000149325&selectedFlexFieldsFacets=%22AttributeChar15%7COCI%7C%7CAttributeChar12%7CLess+than+10+applicants%22",
    "Cloudflare1":"https://www.cloudflare.com/careers/jobs/?department=Engineering&location=Remote+US",
    "Cloudflare2":"https://www.cloudflare.com/careers/jobs/?department=Customer+Support&location=Remote+US"
    # ,"Zscaler":"https://boards.greenhouse.io/zscaler"
    ,"JuniperL":"https://www.linkedin.com/jobs/search/?currentJobId=3557532532&f_C=2240&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
    ,"CloudflareL":"https://www.linkedin.com/jobs/search/?currentJobId=3768699982&f_C=407222&f_TPR=r86400&f_WT=2&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
    ,"teslaL":"https://www.linkedin.com/jobs/search/?currentJobId=3735363379&f_C=15564&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&sortBy=DD"
    ,"nokiaL":"https://www.linkedin.com/jobs/search/?currentJobId=3557536002&f_C=1070&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&sortBy=DD"
    ,"ciscoL":"https://www.linkedin.com/jobs/search/?currentJobId=3767130984&f_C=1063&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"awsL":"https://www.linkedin.com/jobs/search/?currentJobId=3767279587&f_C=2382910&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"amazonL":"https://www.linkedin.com/jobs/search/?currentJobId=3767277264&f_C=1586&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"tiktokL":"https://www.linkedin.com/jobs/search/?currentJobId=3768635136&f_C=33246798&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"captialoneL":"https://www.linkedin.com/jobs/search/?currentJobId=3748698295&f_C=1419&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD&start=25"
    ,"nvidiaL":"https://www.linkedin.com/jobs/search/?currentJobId=3753407228&f_C=3608&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD&start=25"
    ,"aristaL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=80069&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"

    ,"nutanixL":"https://www.linkedin.com/jobs/search/?currentJobId=3769680984&f_C=735085&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"linkedinL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=1337&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"hpeL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=1025&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"arubaL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=162533&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"ibmL":"https://www.linkedin.com/jobs/search/?currentJobId=3769754549&f_C=1009&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"slackL":"https://www.linkedin.com/jobs/search/?currentJobId=3769763314&f_C=1612748&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"intelL":"https://www.linkedin.com/jobs/search/?currentJobId=3748492560&f_C=1053&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
    ,"viasatL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=5770&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"rivianL":"https://www.linkedin.com/jobs/search/?currentJobId=3729762216&f_C=737010&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"p&gL":"https://www.linkedin.com/jobs/search/?currentJobId=3727618774&f_C=1116&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"comcastL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=1703&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"dellL":"https://www.linkedin.com/jobs/search/?currentJobId=3769389016&f_C=1128%2C15088102&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"microsoftL":"https://www.linkedin.com/jobs/search/?currentJobId=3769838643&f_C=1035&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"lumenL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=47664328&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"binanceL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=13336409&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"tolokaL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=71852210&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"yahooL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=1288&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"veritasL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=10003324&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"googleL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=1441&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"metaL":"https://www.linkedin.com/jobs/search/?currentJobId=3725959008&f_C=10667&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"netflixL":"https://www.linkedin.com/jobs/search/?currentJobId=3751398825&f_C=165158&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"charterL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=4561&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"hughesL":"https://www.linkedin.com/jobs/search/?currentJobId=3207979919&f_C=3569&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"verizonL":"https://www.linkedin.com/jobs/search/?currentJobId=3557531560&f_C=1094%2C1103&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"walmartL":"https://www.linkedin.com/jobs/search/?currentJobId=3769856994&f_C=11174522%2C2646&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"gfiberL":"https://www.linkedin.com/jobs/search/?currentJobId=3752162716&f_C=2171947&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"gskL":"https://www.linkedin.com/jobs/search/?currentJobId=3748697819&f_C=1399&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"valeroL":"https://www.linkedin.com/jobs/search/?currentJobId=3769837556&f_C=252536&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"verkadaL":"https://www.linkedin.com/jobs/search/?currentJobId=3557532519&f_C=12699415&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"akamaiL":"https://www.linkedin.com/jobs/search/?currentJobId=3751589131&f_C=3925&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"philipsL":"https://www.linkedin.com/jobs/search/?currentJobId=3769846083&f_C=1090&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"snowflakeL":"https://www.linkedin.com/jobs/search/?currentJobId=3557532519&f_C=3653845&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
,"samsaraL":"https://www.linkedin.com/jobs/search/?currentJobId=3557532519&f_C=6453825&f_JT=F&f_TPR=r86400&geoId=103644278&keywords=engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD"
# ,"":""


}

patterns = [
    '"[A-Za-z/ ]+ [0-9]+ jobs" id="Category',
    '"total_results">[0-9]+</span> results',
    'Open Positions <strong> [0-9]+</strong>',
    '>Jobs</span>\n.*<span class="search-context-button__pill-counter".*?>[0-9]+</span>',
    '"https://boards.greenhouse.(.*?)"',
    '"https://boards.greenhouse.(.*?)"'
    # ,'"/zscaler/jobs/(.*?)\n(.*?)\n(.*?)United States'
    ,'lcount'
    ,'lcount'
    ,'lcount'
    ,'lcount'
    ,'lcount'
    ,'lcount'
    ,'lcount'
    ,'lcount'
    ,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'
,'lcount'

]

lknd_patterns = [
    '>([0-9]+)\sresults<',# count of jobs with login
    '>([0-9]+)\s(?:[A-Za-z]+\s)+\((?:[A-Za-z0-9]+(?: [A-Za-z0-9]+)+)\)</t', # count of jobs without login
    '<a class="base-card__full-link absolute(?:.|\n)*?<span class="sr-only">(?:\s|\n)*([\s|\w|\-|\,|\(|\)]*?)(?:\s|\n)*<' # job titles
]

prev_match={}
#init prev_match
if False: #manually enable this via user only if the file doesnt exist and needs newly creation
    prev_match = urls.copy() #init prev_match without file
    for comp_name in prev_match:
        prev_match[comp_name]=""
else :# init prev_match with file
    prev_match = read_from_file_dict()

#verification of the files content
for url_name in prev_match:
    print (prev_match[url_name])
# print(urls)

if len(urls) != len(patterns):
    logger.error("Error urls array "+str(len(urls))+" and patterns array "+str(len(patterns))+" mismatch")
    sys.exit(1)

while True:
    for url_name, pattern in itertools.zip_longest(urls, patterns):
        try:
            # open some url
            driver.get(urls[url_name])
            print("=== LOG: " + "opened url: "+url_name+"    @"+datetime.now().strftime("%Y-%m-%d %I:%M %p"))
        except Exception as e:
            logger.error("Error during url open method: %s", str(e))
        time.sleep(6)
        try:
            source_page = get_source()
            print("=== LOG: "+"retrieved source")
        except Exception as e:
            logger.error("Error during getting source method: %s", str(e))
        # print(type(source_page))
        # check_pattern = re.compile(r'"[A-Za-z/ ]+ [0-9]+ jobs" id="Category', re.IGNORECASE)
        # pattern = ''
        try:# the regex checking part
            if pattern == "lcount":# implement the linkedin count mechanism
                curr_count = re.findall(lknd_patterns[0],source_page)
                # curr_titles = re.findall(lknd_patterns[1],source_page)
                all_matches = curr_count
                print("=== LOG: " + "filtered patterns linkedin")
                print(all_matches)
            else:# implement general pattern check
                all_matches =  re.findall(pattern,source_page)
                print("=== LOG: "+"filtered patterns")
                print(all_matches)
        except Exception as e:
            logger.error("Error during regex find method: %s", str(e))

        try:# prev file check and notification section
            if url_name in prev_match.keys():#if the company name is already present in the prev_file
                if prev_match[url_name] == all_matches or len(all_matches) == 0:# no changes section
                    print("=== LOG: " + "------------- NO MODIFICATIONS")
                    # if len(all_matches) == 0:
                    #     print("=== LOG: " + "------------- NO MODIFICATIONS (no matches returned in regex find)")
                else :# website changed section
                    print("=== LOG: " + "------------- website CHANGED ")
                    if pattern == "lcount":  # only for linkedin special cases
                        try:
                            if len(all_matches) != 0:# only when a valid jobs page is shown by linkedin
                                if len(prev_match[url_name]) == 0 : # in case prev_match has recorded invalid count, correcting to 0
                                    prev_match[url_name] = ['0']
                                    print("=== LOG: " + "prev_match has recorded invalid count, correcting to 0")
                                if all_matches[0] != "" and prev_match[url_name][0]<all_matches[0]:
                                    print("=== LOG: " + "linkedin count INCREASED from "+str(prev_match[url_name][0])+" to "+str(all_matches[0]))
                                    try:
                                        # send notifcaiton to tele
                                        # bot initialization
                                        bot = Bot(token=token)
                                        send_message(bot, "Website for " + url_name + " has changed [" + urls[url_name] + "] orignal text = " + str(
                                            prev_match[url_name]) + "\n\n new text = " + str(all_matches))
                                    except Exception as e:
                                        logger.error("Error during tele send method: %s", str(e))
                                        try:
                                            bot = Bot(token=token)
                                            send_message(bot, "Website for " + url_name + " has changed [" + urls[
                                                url_name] + "] orignal data length = " + str(len(
                                                prev_match[url_name])) + "\n\n new data length= " + str(len(all_matches)))
                                        except Exception as e:
                                            logger.error("Error during tele send method and even in sending the error to tele: %s", str(e))
                                elif all_matches[0] != "" and prev_match[url_name][0]>all_matches[0]:
                                    print("=== LOG: " + "linkedin count DECREASED from "+str(prev_match[url_name][0])+" to "+str(all_matches[0]))
                                else :
                                    print("=== LOG: " + "linkedin count NO CHNAGE ")
                        except Exception as e:
                            logger.error("Error during getting source method linkedin check: %s", str(e))

                    else:# notify for general websites change
                        try:
                            #send notifcaiton to tele
                            # bot initialization
                            bot = Bot(token=token)
                            send_message(bot, "Website for "+url_name+" has changed ["+urls[url_name]+"] orignal text = "+str(prev_match[url_name])+"\n\n new text = "+str(all_matches))
                        except Exception as e:
                            logger.error("Error during tele send method: %s", str(e))
                            try:
                                bot = Bot(token=token)
                                send_message(bot,"Website for "+url_name+" has changed ["+urls[url_name]+"] orignal data length = "+str(len(prev_match[url_name]))+"\n\n new data length= "+str(len(all_matches)))
                            except Exception as e:
                                logger.error("Error during tele send method and even in sending the error to tele: %s", str(e))

                    prev_match[url_name] = all_matches # updated the prev_match array if changes found in website
            else:# if company name not present then, add this to the prev_match list
                prev_match[url_name] = all_matches
                print("=== LOG: " + " added new link to prev file")
        except Exception as e:
            logger.error("Error during getting source method: %s", str(e))



        # print("=== LOG: " + "checking patterns from saved file ")
        # if prev_match[url_name] == all_matches:
        #     print("=== LOG: " + "nothings changed ")
        # else :
        #     #notify
        #     print("=== LOG: " + "website  changed ")
        #     prev_match[url_name] = all_matches

        print("=== LOG: "+" Moving to next !")
        print ()

    save_to_file(prev_match)
    print("=== LOG: " + "saving to file")
    time.sleep(60)



# regex check that can be done for the HPE site : "[A-Za-z/ ]+ [0-9]+ jobs" id="Category

sys.exit(1)



'''
pending tasks :
- implement a diff checker for the saved content and message only the diff checked part
- for linkedin, the 'resposted' thing is there only when logged in 

'''