import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
