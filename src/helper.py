from uuid import uuid4

from config import keys

import imaplib
import email
import json
import hashlib
import hmac
import time
import requests


def fetch(subject):
    url = 'https://accounts.google.com/o/oauth2/token'

    post_args = {
        'grant_type': 'refresh_token',
        'client_id': keys.GMAIL_CLIENT_ID,
        'client_secret': keys.GMAIL_CLIENT_SECRET,
        'refresh_token': keys.GMAIL_REFRESH_TOKEN
    }

    email_id = 'skyborne.reservations@gmail.com'
    access_token = requests.post(url, data=post_args).json()['access_token']
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (email_id, access_token)

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.debug = 4
    mail.authenticate('XOAUTH2', lambda x: auth_string)
    mail.select('INBOX')

    result, data = mail.search(None, 'ALL')

    ids = data[0]
    id_list = set(ids.split())

    ticket = None;

    for identity in id_list:
        result, data = mail.fetch(identity, '(RFC822)')

        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')

        message = email.message_from_string(raw_email_string)

        if subject in message['subject']:
            ticket = raw_email_string.rstrip()
            mail.store(identity, '+FLAGS', '\\Deleted')
            mail.expunge()

    return ticket


def parse(mail):
    url = "https://api.edison.tech/v1/discovery"

    api_key = keys.EDISON_API
    api_secret = keys.EDISON_SECRET

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
    ).hexdigest()

    response = requests.post(url, data=data)

    return json.dumps(response.json(), indent=2)


def serve(subject):
    timeout = time.time() + 15
    mail = fetch(subject)

    while True:
        if mail or time.time() > timeout:
            return parse(mail)
        else:
            mail = fetch(subject)


def generate_key():
    return json.dumps({'id': str(uuid4().hex[12:]).upper()}, indent=2)
