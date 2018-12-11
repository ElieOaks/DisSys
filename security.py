from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode

def make_keys():   

    random_generator = Random.new().read
    #generate pub and priv key
    priv_key = RSA.generate(1024, random_generator)
    publ_key = priv_key.publickey()

    return (priv_key, publ_key)

def encrypt_message(message):

    (priv_key, publ_key) = make_keys()
    encrypted_message = publ_key.encrypt(message.encode('utf-8'), 32)
    print ('\nYour encrypted message is:\n \n', encrypted_message)
    return (encrypted_message, priv_key)

def main():
    (encrypted_message, priv_key)= encrypt_message('Wassup') 
    decrypted = priv_key.decrypt(encrypted_message)
    decrypted_message = decrypted.decode('UTF-8')
    print ('\nYour decrypted message is:' , decrypted_message, '\n')

main()

'''
   with open('private.pem', 'w') as priv_file:
        tostring = byte_priv.decode('UTF-8')
        priv_file.write(tostring)

    
    with open('private.pem', 'r') as privfile:
        pr_key = RSA.importKey(privfile.read())
        byte_priv = pr_key.exportKey(format='PEM')

    byte_priv = pr_key.exportKey(format='PEM')
    byte_pub  = pu_key.exportKey(format='PEM')
    '''
    