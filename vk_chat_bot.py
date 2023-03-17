import os
import vk_api
import logging

from dotenv import load_dotenv
from dialog_flow import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    load_dotenv()
    vk_api_token = os.getenv("VK_API_TOKEN")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    vk_session = vk_api.VkApi(token=vk_api_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)
