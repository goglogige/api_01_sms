import os
import time
import logging

import requests
from twilio.rest import Client
from dotenv import load_dotenv


logging.basicConfig(
    filename='homework.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
)


load_dotenv()
v = os.getenv('V_VALUE')
token = os.getenv('VK_TOKEN')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
from_value = os.getenv('NUMBER_FROM')
to_value = os.getenv('NUMBER_TO')

client = Client(account_sid, auth_token)


def get_status(user_id):
    vk_method = 'users.get'
    data = {
        'user_ids': user_id,
        'fields': 'online',
        'v': v,
        'access_token': token,
    }
    try:
        response = requests.post(f'https://api.vk.com/method/{vk_method}', params=data)
        user_info = response.json()['response'][0]
        online_status = user_info['online']
    except (ValueError, KeyError) as error:
        logging.error(error)
        return error
    else:
        logging.info("Success, it's work!")
        return online_status


def sms_sender(sms_text):
    message = client.messages \
        .create(
            body=sms_text,
            from_=from_value,
            to=to_value,
        )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
