#!/usr/bin/python3

import requests

url = "https://lcab.smsint.ru/json/v1.0/sms/send/text"

data = {
    "messages": [
        {
            # "recipient": "79099117110",
            # "recipient": "89207557733",
            "recipient": "89252470710",
            "recipientType": "recipient",
            "id": "id0123456789",
            "source": "iDance",
            "timeout": 180,
            "shortenUrl": True,
            "text": "123456 - код подтверждения телефона. iDance"
        }
    ],
    "validate": False
}

token = "ienzrivl1z6jzeqdu8be0dy7d20q3v87jtga4sdhwmdwug71uwn6r9o0bpoxd3hi"
headers={"Content-Type": "application/json", "X-Token": token}

r = requests.post(url, headers=headers, json=data)
print(f"{r.status_code=}, {r.json()=}")
