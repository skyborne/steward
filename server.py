#!/usr/bin/env python3

# Check for email and download the email

from uuid import uuid4

import os
import binascii

def generate_key():
    return binascii.hexlify(os.urandom(2)).decode()

print(generate_key())
