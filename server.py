#!/usr/bin/env python3

from uuid import uuid4

import imaplib
import email
import json
import hashlib
import hmac
import time
import requests

def generate_key():
    return uuid4()

def fetch_mail(uuid):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("skyborne.info@gmail.com", open('.keys/GMAIL', 'r').readline().rstrip())
    mail.list()
    mail.select("inbox")

    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = data[0][1]
    raw_email_string = raw_email.decode("utf-8")

    message = email.message_from_string(raw_email_string)

    return {message['subject']: raw_email_string}

def parse_mail(email, uuid):
    url = "https://api.edison.tech/v1/discovery"

    api_key = open('.keys/EDISON', 'r').readline().rstrip()
    api_secret = open('.keys/EDISON_SECRET', 'r').readline().rstrip()

    email = fetch_mail(uuid)

    data = {
        'email': email,
        'api_key': api_key,
        'timestamp': int(time.time())
    }

    base_string = 'POST&/v1/discovery'

    for k in sorted(data):
        base_string += '&' + k + '=' + str(data[k])

    data['signature'] = hmac.new(
        api_secret.encode('utf-8'),
        base_string.encode('utf-8'),
        hashlib.sha1
    ).hexdigest().decode('utf-8')

    response = requests.post(url, data=data)
    return json.dumps(response.json(), indent=2)


def main():
    print(fetch_mail(1))

if __name__ == "__main__":
    main()
