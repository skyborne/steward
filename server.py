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
    email_id = 'skyborne.reservations@gmail.com'
    access_token = 'access_key'
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (email_id, access_token)

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.debug = 4
    mail.authenticate('XOAUTH2', lambda x: auth_string)
    mail.select('INBOX')

    ids = data[0]
    id_list = ids.split()

    for identity in id_list:
        result, data = mail.fetch(identity, "(RFC822)")

        raw_email = data[0][1]
        raw_email_string = raw_email.decode("utf-8")

        message = email.message_from_string(raw_email_string)

        if message['subject'] == uuid:
            return { 'email': raw_email_string }
        else:
            return 'nil'

def parse_mail(email, uuid):
    url = "https://api.edison.tech/v1/discovery"

    api_key = open('.keys/EDISON', 'r').readline().rstrip()
    api_secret = open('.keys/EDISON_SECRET', 'r').readline().rstrip()

    mail = fetch_mail(uuid)

    data = {
        'email': mail,
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
