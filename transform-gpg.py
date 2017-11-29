#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 23:31:52 2017

@author: eckart
"""

import ironpipe
import gnupg
import sys

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
            ironpipe.exit('Data encryption error: {}'.format(err))

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
                id = id[0] # Assume the first fingerprint is the imported key
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
            ironpipe.exit('Data encryption error: {}'.format(err))

    # Write the encrypted string to the output file and update content type
    try:
        output.write(str(encrypted_data))
        ironpipe.set_metadata('content-type', 'application/pgp-encrypted')
    except Exception as err:
        ironpipe.exit('Data write error: {}'.format(err))    

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
            ironpipe.exit('Data decryption error: {}'.format(err))

    elif secret_type == 'pki':
        try:
            # import public key
            import_result = gpg.import_keys(secret['config']['private_key'])
            id = import_result.fingerprints

            # import_keys returns an empty list if it was not able to parse the key            
            if not id:
                raise ValueError('Bad private_key value')
 
        except Exception as err:
            ironpipe.exit('Key import error {}'.format(err))
            
        # Decrypt the input data using the imported key
        try:
            encrypted_data = input.read()
            decrypted_data = gpg.decrypt(encrypted_data)
            if not decrypted_data.ok:
                raise Exception(decrypted_data.status)
        except Exception as err:
            ironpipe.exit('Data decryption error: {}'.format(err))
    
    # Write file as binary data to support encrypted images or binary file types
    try:
        output.buffer.write(decrypted_data.data)     
    except Exception as err:
        ironpipe.exit('Data write error: {}'.format(err))  

    
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
        ironpipe.exit('Missing secret.')

    # Confirm that secret has a config section and appropriate values
    secret_config = secret.get('config')
    if not secret_config or not isinstance(secret_config, dict):
        ironpipe.exit('Secret missing config {}'.format(secret))

    # Confirm that secret is a dictionary and either token or PKI type
    secret_type = secret.get('action', '').lower()    
    if secret_type not in ['pki', 'token']:
        ironpipe.exit("Secret must be either 'token' or 'pki'.")

    if secret_type == 'token':
        token = secret_config.get('token')
        if not token or not isinstance(token, str):
            ironpipe.exit("Secret missing 'token' value.")
    elif secret_type == 'pki':
        if mode == 'encrypt':
            public_key = secret_config.get('public_key')
            if not public_key or not isinstance(public_key, str):
                ironpipe.exit("Secret missing 'public_key' value.")
        elif mode == 'decrypt':
            private_key = secret_config.get('private_key')
            if not private_key or not isinstance(private_key, str):
                ironpipe.exit("Secret missing 'private_key' value.")

#
# Config values - mode (encrypt, decrypt, verify), secret
#
def cipher():
    '''
    '''
    mode = ironpipe.get_config('mode')
    secret = ironpipe.get_config('secret')
        
    # Confirm that mode is set and a string
    if not mode or not isinstance(mode, str):
        ironpipe.exit('Need to specify mode.')
    else:
        mode = mode.lower()

    # Validate that secret matches mode
    validate_secret(secret, mode)

    # Confirm that mode is known
    if mode not in MODE_MAP_FUNCTIONS:
        mode = ', '.join([i for i in MODE_MAP_FUNCTIONS])
        ironpipe.exit("Mode must be one of: {}.".format(mode))                      
                
    # Encrypt / unencrypt / validate input file        
    MODE_MAP_FUNCTIONS[mode](sys.stdin, sys.stdout, secret)

    return 0

#
#        
def main():   
    return cipher()

if __name__ == '__main__':
    main()

'''


    if secret['action'] is 'token':
        foo = gpg.encrypt('hello world', recipients=None, passphrase='hello', symmetric=True)

    
    try:
        with gzip.open(input.buffer) as file:
            data = file.read()
    except Exception as err:
        ironpipe.exit('Data read error: {}'.format(err))

    # Write file as binary data to support encrypted images or binary file types
    try:
        output.buffer.write(data)     
    except Exception as err:
        ironpipe.exit('Data write error: {}'.format(err))



    cipher_algo = ironpipe.get_config('cipher-algo')
    import_result = gpg.import_keys(private_key + public_key)
    import_result.fingerprints
    
    out = gpg.encrypt('hello', '3A7C4988F28AAE5C9074864BF3293A4CCD0FCFB9')
    str(out)

        
    gpg = gnupg.GPG(verbose=None)
    foo = gpg.encrypt('hello world', recipients=None, passphrase='hello', symmetric=True)
    bar = gpg.decrypt(foo.data, passphrase='hello')
    
    baz = gpg.decrypt(foo.data)
    
    ssh-keygen - create public and private key
'''

    
private_key = '''
-----BEGIN PGP PRIVATE KEY BLOCK-----

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
tr52aJm+m7QMC4tt1JCy3FpenZI2N6h5wmwxDA==
=Pat3
-----END PGP PRIVATE KEY BLOCK-----
'''
   
public_key = '''
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFocVBoBCAC7wNHOWcU4Uc/0XLnCPmAEFcn4fMNw2PxI1B+VOKWbr7kTxFpB
IMxbvaNtW9hDfuwXrWlUVQhIpAzfAIPjIshDQgIE/Mee7je0bu/vDPNW9VtsaFTw
53WDNlN/HWfDRtL+qqQVHbucPFgn3OVBjtNFLns4HQKelW1wlTR6vSZRNRkGcVix
/fMnSSlMPfhmgY2jctbjeotykSvl+9J6xBMQk3m+/DUkQjj44gTAeMG5Rmp4iD37
RXm8OW8kzTF+wI6dDBvKjY6NvvVfJUiU80hPUHfSIlm4AU9yGOfnHiEcA5OdrAFS
n9yjelmYpH9532RP1sDFRt0FNvK+0zMcxvL7ABEBAAG0DkVja2FydCBXYWx0aGVy
iQFUBBMBCAA+FiEEOnxJiPKKrlyQdIZL8yk6TM0Pz7kFAlocVBoCGwMFCQPCZwAF
CwkIBwIGFQgJCgsCBBYCAwECHgECF4AACgkQ8yk6TM0Pz7kIHwf9HzS7xTfgZyXh
qWxlhBymR4xFIXRlgpA2jUAE8OLWIaqOTDC7cn2UkY7QueR7Prbm8ZcIfotb3KNA
X+nnB5C5AOauQ/5XHQAe8WgRQXk71WkejqyP5BQUf8brnzsCv763IYUyK/k8WkAk
CPEMBn30+JNGvV2EOX6rTDMvqgcCvL8J/7MvWdXIIWDGECpr8+Pwq6+Ay9AHYLWn
xOxrB3qdTEfL/WeH4foifxb8DShM3vnj8W6FXjDY+Phx5NTeoHsLRXSI4NCNHtDB
1AxgACSDrQ2Laa2fPJjldTMgNqrbuQwF09urDcsfMOI7zqyBuWo7Kl6iMzCPJTdN
rldX1vD1m7kBDQRaHFQaAQgAumyjIuVOMDxyItLnzr7INuiQYaTQJgl8ohY8YfO8
CtVx5D06vJMInf7lKaFJtfdVd9D+UVlot0HAFYg90Whejynq5gbbeouh0VtGehhb
1PAm0o96sIgLBLBGgy1zp8HUYWZjgUKzjojlZMy5RMZN0bwVHiXxTaFyR6J6qyJr
8Q/XyoIjRLHBOO8aZLAtsiA4UpBL3XiCvIW1R/PFzmYiB7OsVJ9gNUC9Ko5YhI96
u1dWpbGh1cjvG4sUlshx6jZpuPKv6mjPSjFG7tdiCR3XgI9ZUv3QGkosWqFouRoi
Pe5QdaywYnipZi/DszV7zYGeP53qgHQDxtXKgadt9WFawwARAQABiQE8BBgBCAAm
FiEEOnxJiPKKrlyQdIZL8yk6TM0Pz7kFAlocVBoCGwwFCQPCZwAACgkQ8yk6TM0P
z7naiQf8C5xbJegffhr5qBUpqtg7HMpNhVKC/kimmSS5Tee7VUt/HbvdN1tpPo5o
CcimXJP3w2HKszUxoIYljAEQCG/vENNf2Srqg9zwEU0jQrx6JM0mI5t7MkI2dc2Y
1ywbiWwtWO18rdpKC1UmgCp9L52JqsArdQbVFginpeDjLCYu3qcFrU9G0V35uMvj
ZXLvLe0isho8A2A0CxIbrO/5VJFOwvcAgCzfr1NWSE2cs8czszK4RzFg3YZYfGBu
TGuzBfRjUsVL6kdSyw8LbdL/NK3Z8Irea7wjZtxxZ/7v2hO4Z1vEopRNtr52aJm+
m7QMC4tt1JCy3FpenZI2N6h5wmwxDA==
=j4ae
-----END PGP PUBLIC KEY BLOCK-----
'''

encrypted_data = '''
-----BEGIN PGP MESSAGE-----

hQEMA8Fx3F70LSDJAQgAs/fyMmuP/dOkbHNLI7dh1Z76YICLVqz3xBJihUgPf6/h
0DHqKnE6pe9svu3Q0hJQuw5X5CT5Kb7nKPhMD1Fj1BLlM2t4996pF4hgpVOlHaWT
DSQ9lbpsnU6UoU+s9b1zxxPInGfqgYOFiIhRvf+b6B80tWu6RseiwuVauFEG/5vh
rqw4A8PhBcEYImHM+iSKT2t8dExpI19IQbMICODQ0a8Ns4rIM7nxM0Bt4wPQbvBe
+8g44iIuJHHOZt1itCfRdGeGfIEweP9BkuEPv9WakCMqcC36B4aOWqTrLu3Lt55x
+TF7aAJnssrd6Gh0IYbO1RY0w20HdTBd03kLkGFX7dI7ARxJpHZWf6jXvJUW4s5u
sMV4VJCp8DKdYacVeLbSzD9RHZgLkc251YoOVjQPF7BIJQvHfQ+Yc9NcIVE=
=ePP1
-----END PGP MESSAGE-----
'''
 

