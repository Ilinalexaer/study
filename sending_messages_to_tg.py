#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def send_telegram(text: str):
    token = os.getenv('TOKEN')
    url = "https://api.telegram.org/bot"
    channel_id = "-1001894153674"
    url += token
    method = url + "/sendMessage"
    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")
