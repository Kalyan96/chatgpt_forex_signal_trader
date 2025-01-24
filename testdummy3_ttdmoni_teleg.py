import time,pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

def get_current_updates():
    class_name = "latestUpdates_list__2tn1D"
    news_list_container = driver.find_element(By.CLASS_NAME, class_name)
    news_updates = news_list_container.find_elements(By.TAG_NAME, "li")
    return ["- "+update.text+"\n" for update in news_updates]

def save_to_file(updates):
    with open(store_file, 'w') as file:
        file.write(str(updates))

def read_from_file():
    with open(store_file, 'r') as file:
        return file.read()

def send_message(bot, message):
    global chat_id
    bot.send_message(chat_id=chat_id, text=message)

def echo(update, context):
    user_message = update.message.text
    update.message.reply_text(f'You said: {user_message}')

    # After replying, send a message
    # send_message(context.bot, update.message.chat_id, "This is an additional message.")





# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
token = '6538387137:AAEtL9aJvWxS_LLTW9vVn3gtfWd4aeM0Nlk'
chat_id = "6020027159"

# initialize the driver
driver = webdriver.Chrome()
#add a log message after this  line
print("=== LOG: "+"chrome driver created")

store_file = "testdummy3_ttdmonitor_lastupdate.txt"

#bot initialization
bot = Bot(token=token)
# updater = Updater(bot=bot)
# dispatcher = updater.dispatcher
# dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, echo))
# updater.start_polling()
print ("chatbot initialized")

# open some url
driver.get('https://online.tirupatibalaji.ap.gov.in/home/dashboard')
print("=== LOG: "+"opened url")
time.sleep(10)
# classn = "latestUpdates_containerMobile__1l6vi"
# class1 = "card_scroll"
# news_container = driver.find_element(By.CLASS_NAME, class1)
# print(news_container.text)
# before_click_source = driver.page_source
# print(before_click_source)



# class_name = "latestUpdates_list__2tn1D"
# news_list_container = driver.find_element(By.CLASS_NAME, class_name)
#
# # Find all the <li> elements within the container
# news_updates = news_list_container.find_elements(By.TAG_NAME, "li")
#
# # Iterate through the <li> elements and print the text content of each one
# for update in news_updates:
#     print(update.text)





#reads the old news
current_updates = read_from_file()
# print (current_updates)
# Periodically check for new updates
while True:
    new_updates = get_current_updates()

    # Check if there are any new updates
    if str(new_updates) != str(current_updates):
        print("---------- New updates found:")
        send_message(bot, "---------- New updates found:")
        for update in new_updates:
            if update not in current_updates:
                send_message(bot, update)
                print("- "+update)

        # Update the current updates variable with the new updates
        current_updates = new_updates
        save_to_file(new_updates)
    else :
        print("=== No new updates found")

    driver.refresh()
    print("=== LOG: "+"refreshed the page")
    time.sleep(600)  # Wait for 60 seconds before checking again

    # break#comment this to check as a loop
