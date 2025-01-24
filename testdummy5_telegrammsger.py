import time

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
token = '6538387137:AAEtL9aJvWxS_LLTW9vVn3gtfWd4aeM0Nlk'
chat_id = "6020027159"

def send_message(bot, message):
    global chat_id
    bot.send_message(chat_id=chat_id, text=message)

def echo(update, context):
    user_message = update.message.text
    update.message.reply_text(f'You said: {user_message}')

    # After replying, send a message
    # send_message(context.bot, update.message.chat_id, "This is an additional message.")

def bot_init():
    bot = Bot(token=token)
    update_queue = asyncio.Queue()
    updater = Updater(bot=bot)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, echo))

    updater.start_polling()
    print ("chatbot started")
    while True:
        time.sleep(5)
        send_message(bot, "checkeds")
    updater.idle()

if __name__ == '__main__':
    bot_init()