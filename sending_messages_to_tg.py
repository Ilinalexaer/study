#!/usr/bin/env python3
import requests

def send_telegram(text: str):
    token = "5424286381:AAEC9ZJ4TNiFiqSEJ4Sa56hCPpDhLfzeOVY"
    url = "https://api.telegram.org/bot"
    #channel_id = "@new_flat_krisha"
    channel_id = "-1001894153674"
    url += token
    method = url + "/sendMessage"
    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")


#https://api.telegram.org/bot5424286381:AAEC9ZJ4TNiFiqSEJ4Sa56hCPpDhLfzeOVY/sendMessage?chat_id=@new_flat_krisha&text=тест
#"id":-1001894153674
#https://api.telegram.org/bot5424286381:AAEC9ZJ4TNiFiqSEJ4Sa56hCPpDhLfzeOVY/sendMessage?chat_id=-1001894153674&text=тест