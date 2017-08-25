#!/usr/bin/env python

import getopt
import base64
import boto
import os
import sys

def usage():
    print 'get_windows_password.py -i <instance-id>'

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def decrypt_rsa(cipher_text):
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    key = RSA.importKey(open('/Users/amaksimov/.ssh/id_rsa_without_pass', "rb").read())
    cipher = PKCS1_v1_5.new(key)
    password = cipher.decrypt(base64.b64decode(cipher_text), None)
    return password

def get_password(instance_id):
    ec2 = boto.connect_ec2_endpoint(os.getenv('EC2_URL'),
                                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    reservations = ec2.get_all_instances(instance_ids=[instance_id])
    instance = reservations[0].instances[0]
    output = instance.get_console_output()
    base64_encoded_encrypted_pass = find_between(output.output, "<Password>", "</Password>")
    print decrypt_rsa(base64_encoded_encrypted_pass)

try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hi:', []) 
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in options:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt in ('-i', '--instance-id'):
        if arg is not None:
            get_password(arg)
    else:
        usage()
        sys.exit(2)


