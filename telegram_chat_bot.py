import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
from dialog_flow import detect_intent_texts


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

def keep_conversation(update: Update, context: CallbackContext, project_id):
    language_code = "ru"
    answer = detect_intent_texts(
        project_id,
        update.effective_chat.id,
        update.message.text,
        language_code)
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dialogflow_handler = MessageHandler(
        Filters.text & (~Filters.command),
        lambda update, context: keep_conversation(update, context, project_id)
    )
    dispatcher.add_handler(dialogflow_handler)

    updater.start_polling()
