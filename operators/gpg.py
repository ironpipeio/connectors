#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 23:31:52 2017

@author: eckart
"""

import gnupg
import sys

sys.path.append('../lib')
import ironpipe.extension

#
# Encrypt/decrypt files using gpg
#


#
#
def encrypt_file(input, output, secret):
    '''
    '''
    gpg = gnupg.GPG(verbose=None)

    secret_type = secret['action']

    if secret_type == 'token':
        try:
            # symmetrically encrupt file using phassphrase from secret
            # Read from buffer to support binary files
            decrypted_data = input.buffer.read()

            encrypted_data = gpg.encrypt(decrypted_data, recipients=None, passphrase=secret['config']['token'], symmetric=True)
            # check if successful
            if not encrypted_data.ok:
                raise Exception(encrypted_data.status)

        except Exception as err:
            ironpipe.extension.exit('Data encryption error: {}'.format(err))

    elif secret_type == 'pki':
        # cipher_algo = ironpipe.get_config('cipher-algo')
        try:
            # import public key
            import_result = gpg.import_keys(secret['config']['public_key'])
            id = import_result.fingerprints

            # import_keys returns an empty list if it was not able to parse the key
            if not id:
                raise ValueError('Bad public_key value')
            else:
                id = id[0]  # Assume the first fingerprint is the imported key
        except Exception as err:
            ironpipe.exit('Key import error {}'.format(err))

        # Encrypt the input data using the imported key
        try:
            # Read from buffer to support binary files
            decrypted_data = input.buffer.read()

            encrypted_data = gpg.encrypt(decrypted_data, id)
            if not encrypted_data.ok:
                raise Exception(encrypted_data.status)
        except Exception as err:
            ironpipe.extension.exit('Data encryption error: {}'.format(err))

    # Write the encrypted string to the output file and update content type
    try:
        output.write(str(encrypted_data))
        ironpipe.extension.set_metadata('content-type', 'application/pgp-encrypted')
    except Exception as err:
        ironpipe.extension.exit('Data write error: {}'.format(err))


#
#
def decrypt_file(input, output, secret):
    '''
    '''
    gpg = gnupg.GPG(verbose=None)

    secret_type = secret['action']

    if secret_type == 'token':
        try:
            # symmetrically decrypt file using phassphrase from secret
            encrypted_data = input.read()
            decrypted_data = gpg.decrypt(encrypted_data, passphrase=secret['config']['token'])
            if not decrypted_data.ok:
                raise Exception(decrypted_data.status)
        except Exception as err:
            ironpipe.extension.exit('Data decryption error: {}'.format(err))

    elif secret_type == 'pki':
        try:
            # import public key
            import_result = gpg.import_keys(secret['config']['private_key'])
            id = import_result.fingerprints

            # import_keys returns an empty list if it was not able to parse the key
            if not id:
                raise ValueError('Bad private_key value')

        except Exception as err:
            ironpipe.extension.exit('Key import error {}'.format(err))

        # Decrypt the input data using the imported key
        try:
            encrypted_data = input.read()
            decrypted_data = gpg.decrypt(encrypted_data)
            if not decrypted_data.ok:
                raise Exception(decrypted_data.status)
        except Exception as err:
            ironpipe.extension.exit('Data decryption error: {}'.format(err))

    # Write file as binary data to support encrypted images or binary file types
    try:
        output.buffer.write(decrypted_data.data)
    except Exception as err:
        ironpipe.extension.exit('Data write error: {}'.format(err))


#
# map action appropriate function
#
MODE_MAP_FUNCTIONS = {
    'encrypt': encrypt_file,
    'decrypt': decrypt_file
}


#
# Validate the secret matches decryption / encryption mode
#
def validate_secret(secret, mode):

    # Confirm that secret is set and a dictionary
    if not secret or not isinstance(secret, dict):
        ironpipe.extension.exit('Missing secret.')

    # Confirm that secret has a config section and appropriate values
    secret_config = secret.get('config')
    if not secret_config or not isinstance(secret_config, dict):
        ironpipe.extension.exit('Secret missing config {}'.format(secret))

    # Confirm that secret is a dictionary and either token or PKI type
    secret_type = secret.get('action', '').lower()
    if secret_type not in ['pki', 'token']:
        ironpipe.extension.exit("Secret must be either 'token' or 'pki'.")

    if secret_type == 'token':
        token = secret_config.get('token')
        if not token or not isinstance(token, str):
            ironpipe.extension.exit("Secret missing 'token' value.")
    elif secret_type == 'pki':
        if mode == 'encrypt':
            public_key = secret_config.get('public_key')
            if not public_key or not isinstance(public_key, str):
                ironpipe.extension.exit("Secret missing 'public_key' value.")
        elif mode == 'decrypt':
            private_key = secret_config.get('private_key')
            if not private_key or not isinstance(private_key, str):
                ironpipe.extension.exit("Secret missing 'private_key' value.")


#
# Config values - mode (encrypt, decrypt, verify), secret
#
def cipher():
    '''
    '''
    mode = ironpipe.extension.get_config('mode')
    secret = ironpipe.extension.get_config('secret')

    if mode:
        mode = mode.lower()

    # Confirm that mode is set and a string
    if not mode or not isinstance(mode, str) or mode not in MODE_MAP_FUNCTIONS:
        mode = ', '.join([i for i in MODE_MAP_FUNCTIONS])
        ironpipe.extension.exit("Required attribute 'mode' must be one of: {}.".format(mode))

    # Validate that secret matches mode
    validate_secret(secret, mode)

    # Encrypt / unencrypt / validate input file
    MODE_MAP_FUNCTIONS[mode](sys.stdin, sys.stdout, secret)

    return 0


#
#
def main():
    return cipher()


if __name__ == '__main__':
    main()
