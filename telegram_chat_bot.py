import os
import time
import logging
import telegram

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
from dialog_flow import detect_intent_texts
from telegram_logs_handler import TelegramLogsHandler


NAME = os.path.basename(__file__)

logger = logging.getLogger(__name__)


def keep_conversation(update: Update, context: CallbackContext, project_id):
    language_code = "ru"
    flag = True
    while flag:
        try:
            _, answer = detect_intent_texts(
                project_id,
                update.effective_chat.id,
                update.message.text,
                language_code)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=answer
            )
            flag = False
        except telegram.error.NetworkError as error:
            logger.error(NAME, error)
            time.sleep(1)
        except Exception as error:
            logger.exception(NAME, error)
            continue


def main():
    load_dotenv()

    telegram_notify_token = os.environ["TELEGRAM_NOTIFY_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    notify_bot = telegram.Bot(token=telegram_notify_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(notify_bot, chat_id))

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher

    dialogflow_handler = MessageHandler(
        Filters.text & (~Filters.command),
        lambda update, context: keep_conversation(update, context, project_id)
    )
    dispatcher.add_handler(dialogflow_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
