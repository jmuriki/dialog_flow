import os
import random
import logging
import vk_api as vk

from dotenv import load_dotenv
from dialog_flow import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main():
    load_dotenv()
    vk_api_token = os.getenv("VK_API_TOKEN")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
        # if event.type == VkEventType.MESSAGE_NEW:
        #     print('Новое сообщение:')
        #     if event.to_me:
        #         print('Для меня от: ', event.user_id)
        #     else:
        #         print('От меня для: ', event.user_id)
        #     print('Текст:', event.text) 


if __name__ == '__main__':
    main()
