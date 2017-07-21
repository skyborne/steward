#!/usr/bin/env python3

from uuid import uuid4

import imaplib
import email

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

    return message

def parse_mail(email):
    pass

def main():
    print(fetch_mail(1))

if __name__ == "__main__":
    main()
