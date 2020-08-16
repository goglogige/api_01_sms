import os
import time

import requests
from twilio.rest import Client
from dotenv import load_dotenv


def get_status(user_id):
    load_dotenv()
    token = os.getenv('vk_token')
    data = {
        'user_ids': user_id,
        'fields': 'online',
        'v': '5.92',
        'access_token': token,
    }
    response = requests.post('https://api.vk.com/method/users.get', params=data)
    user_info = response.json()['response'][0]
    online_status = user_info['online']
    return online_status


def sms_sender(sms_text):
    load_dotenv()
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    from_value = os.getenv('NUMBER_FROM')
    to_value = os.getenv('NUMBER_TO')
    client = Client(account_sid, auth_token)
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
