#!/usr/bin/python3

import argparse
import requests
import random
import sys
from datetime import datetime

parser = argparse.ArgumentParser(description='Test smsint service.')
parser.add_argument('-p', '--phone', type=str, default="89099117110", help='phone number to send sms (default: %(default)s)')
args = parser.parse_args()

# print(f"{args.phone=}")

code = str(random.randint(0, 999999)).zfill(6)
# print(f"{code=}")
# exit()

msgid = datetime.now().strftime("%Y/%m/%d_%H:%M:%S_") + str(random.randint(0, 999999)).zfill(6)

url = "https://lcab.smsint.ru/json/v1.0/sms/send/text"

data = {
    "messages": [
        {
            "recipient": args.phone,
            "recipientType": "recipient",
            "id": msgid,
            "source": "iDance",
            "timeout": 180,
            "shortenUrl": True,
            "text": f"{code} - код подтверждения телефона. iDance"
        }
    ],
    # "validate": False
    "validate": True
}

token = "ienzrivl1z6jzeqdu8be0dy7d20q3v87jtga4sdhwmdwug71uwn6r9o0bpoxd3hi"
headers={"Content-Type": "application/json", "X-Token": token}

r = requests.post(url, headers=headers, json=data)

def processResponse(r, msgid):
    if not r.headers.get('content-type') == 'application/json':
        return False, "Error: content-type is not application/json", None

    r_json = None
    try:
        r_json = r.json()
    except ValueError:
        return False, "Error: get json", None

    if r.status_code != 200:
        return False, f'Error: replay status is not 200, [status_code={r.status_code}, reason={r.reason}, json = {r_json}]', None

    if "success" in r_json and r_json["success"] == True and "result" in r_json and "messages" in r_json["result"]:
        msgSendStatus = False
        for msg in r_json["result"]["messages"]:
            if "id" in msg and msg["id"] == msgid and 'success' in msg and msg["success"] == True:
                msgSendStatus = True
                break
        if msgSendStatus:
            return True, None, r_json

    return False, f"Error: sms send failed, json = {r_json}", None

result, errorMsg, r_json = processResponse(r, msgid)

if not result:
    sys.stderr.write(f'{errorMsg}\n')
    exit(1)

sys.stderr.write(f"Sms send ok: status_code = {r.status_code=}, json = {r_json}\n")

print(f"code = [{code}] was send to phone {args.phone}\n")
