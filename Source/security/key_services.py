#!/usr/bin/python
import os
import random
import re
import string
import json
from pathlib import Path
import Crypto
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from configobj import ConfigObj


class Messenger:
    def __init__(self):
        self.session_key = None
        self.cipher_rsa: RSA.RsaKey = None
        self.enc_session_key: PKCS1OAEP_Cipher = None
        # self.cipher_aes = None
        self.ciphertext, self.tag = ("", "")
        self.security_manager = None
        self.config = None
        self.config_dictionary: dict = None
        self.configfile = ''.join(str(Path(os.getcwd()).parent) + f"\\src\\security\\config.bin")
        self.keyfile = ''.join(str(Path(os.getcwd()).parent) + f"\\src\\security\\private_key.pem")

    def init(self, keyfile="private_key.pem", configfile="config.bin"):
        self.keyfile = keyfile
        self.configfile = configfile
        if configfile is "config.bin":
            if self.unlock_file(self.keyfile):
                self.session_key = self.get_session(self.keyfile)
                # Encrypt the session key with the public RSA key
                self.cipher_rsa = RSA.import_key(self.session_key._key)
                self.lock_file(self.keyfile)
                self.lock_file(self.keyfile)
        self.config = self.load_config(configfile=self.configfile, keyfile=self.keyfile)

    def update_config(self, config: ConfigObj):
        try:
            self.config_dictionary = dict({
                "MONGO_SERVER": config['cloud.mongodb']['connection_url'],
                "DATABASES": config['cloud.mongodb']['databases'],
                "CRED_USER": config['cloud.mongodb']['credential_manager']['username'],
                "CRED_PASSWORD": config['cloud.mongodb']['credential_manager']['password'],
                "JOB_MANAGER_ID": config['cloud.mongodb']['job_manager']['username'],
                "JOB_MANAGER_PASS": config['cloud.mongodb']['job_manager']['password'],
                "SCRAPER_ACCOUNT": config['cloud.mongodb']['scraperadmin'],
                "PROXY": config['proxy'],
                "KEYMANAGER": config['keymanager']
            })
        except Exception as e:
            return False
        return self.config_dictionary

    def encrypt_file(self, datafile: str, fileout: str):
        data = open(datafile, "rb").read()
        file_out = open(f"{os.getcwd()}\\src\\security\\{fileout}.bin", "wb")
        recipient_key = RSA.import_key(f"{self.session_key._key}".encode("utf-8"))
        random_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(random_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(random_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

    def get_session(self, keyfile="private_key.pem"):
        if self.unlock_file(keyfile):
            session: PKCS1OAEP_Cipher = PKCS1_OAEP.new(open(keyfile).read())
            self.lock_file(keyfile)
            return session

    def unlock_file(self, filename):
        try:
            os.system(f"chmod 644 {filename}")
            return True
        except Exception as e:
            print(e)
            return False

    def lock_file(self, filename):
        try:
            os.system(f"chmod 644 {filename}")
        except Exception as e:
            print(e)
            return False

    def decrypt_data(self, data):
        session = self.get_session(self.keyfile)
        rsa_key = RSA.importKey(session._key)
        enc_session_key, nonce, tag, ciphertext = \
            [data.read(x) for x in (session._key.size_in_bytes(), 16, 16, -1)]
        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(session)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        print(data.decode("utf-8"))

    def decrypt_file(self, datafile):
        try:
            datafile = open(datafile, "rb")
            private_key = RSA.import_key(f"{self.session_key._key}".encode("utf-8"))
            enc_session_key, nonce, tag, ciphertext = \
                [datafile.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
            # Decrypt the session key with the private RSA key
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            # Decrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            return data

        except Exception as e:
            print(e)
            return False

    def load_config(self, configfile="config.bin", keyfile="private_key.pem"):

            if re.search("(?<=\w)*(bin)", configfile):
                config_data = self.decrypt_file(datafile=configfile)
                try:
                    temp_file = ''.join(random.choice(string.ascii_lowercase) for x in range(10)) + ".tmp"
                    with open(f"{str(Path(os.getcwd()))}" + f"\\src\\security\\{temp_file}", "wb") as writeout:
                        writeout.write(config_data)

                    config = ConfigObj(f"{str(Path(os.getcwd()))}" + f"\\src\\security\\{temp_file}")
                    self.config = config
                    self.update_config(config)
                    os.system("rm " + f"{str(Path(os.getcwd()))}" + f"\\src\\security\\{temp_file}")
                    return config
                except Exception as e:
                    print(e)
                    os.system("rm " + f"{str(Path(os.getcwd()))}" + f"\\src\\security\\{temp_file}")
                    return False
            else:
                config = ConfigObj(f"{configfile}")
                if self.update_config(config):
                    return config
                else:
                    print("No configurations found for session!")
                    return False


def main():
    print("main")


if __name__ == "__main__":
    main()
