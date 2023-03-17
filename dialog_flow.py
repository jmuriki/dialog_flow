import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import MessageHandler, Filters
from google.cloud import dialogflow


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


# def echo(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# def start(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    return response.query_result.fulfillment_text


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

    # start_handler = CommandHandler('start', start)
    # dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    dialogflow_handler = MessageHandler(
        Filters.text & (~Filters.command),
        lambda update, context: keep_conversation(update, context, project_id)
    )
    dispatcher.add_handler(dialogflow_handler)

    updater.start_polling()
