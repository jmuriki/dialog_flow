import os
import time
import random
import logging
import telegram
import vk_api as vk

from dotenv import load_dotenv
from dialog_flow import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram_logs_handler import TelegramLogsHandler


logger = logging.getLogger(__name__)


def keep_conversation(event, vk_api, project_id):
    language_code = "ru"
    time_sleep = 0
    while True:
        try:
            distinction_fail, answer = detect_intent_texts(
                project_id,
                event.user_id,
                event.text,
                language_code)
            if not distinction_fail:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=answer,
                    random_id=random.randint(1, 1000)
                )
            return
        except Exception as error:
            logger.exception(error)
            time.sleep(time_sleep)
            time_sleep += 1


def main():
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(process)d %(levelname)s %(message)s",
    )

    telegram_notify_token = os.environ["TELEGRAM_NOTIFY_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    notify_bot = telegram.Bot(token=telegram_notify_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(notify_bot, chat_id))

    vk_api_token = os.getenv("VK_API_TOKEN")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            keep_conversation(event, vk_api, project_id)


if __name__ == '__main__':
    main()
