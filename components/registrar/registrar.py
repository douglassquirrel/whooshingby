#!/usr/bin/python
from base64 import b64encode
from hashlib import sha512
from json import loads
from kropotkin import get_next_fact, store_fact, subscribe
from os import urandom

def generate_salt():
    return b64encode(urandom(24))

def create_hash(salt, password):
    return sha512(salt+password).hexdigest()

subscribe('whooshingby', 'fact', 'registration_request')
while True:
    request = get_next_fact('whooshingby', 'registration_request')
    if not request:
        continue

    name = request['name']
    password = request['password']
    salt = generate_salt()
    hash = create_hash(salt, password)
    content = {'name': name, 'salt': salt, 'hash': hash}
    if not store_fact('whooshingby', 'user', content):
        stderr.write('Could not store user fact, name %s\n' % name)
