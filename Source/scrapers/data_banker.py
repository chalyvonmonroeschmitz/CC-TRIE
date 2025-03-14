#!/usr/bin/python
import asyncio
import os
import sys
import json
from json import JSONDecodeError
from os import walk
from pdf2image import convert_from_path, convert_from_bytes
from archiver import Archiver


class Data_Banker(Archiver):
    def __init__(self):
        super().__init__()

    def store_archives(self, subject, location):
        print("Uploading data files...")
        dbUser = self.key_service.config['cloud.mongodb']['scraperadmin']
        user = self.security_manager.get_dbUser(dbUser['username'])
        cred_user = self.key_service.config['cloud.mongodb']['credential_manager']
        self.security_manager.set_connection_id('scraperadmin', dbUser['password'],
                                                self.key_service.config['cloud.mongodb']['connection_url'])
        data = {}
        file_lists = []
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + "/Data/" + subject + '/' + location + "/data"):
            file_lists.extend(filenames)
            break

        db = self.security_manager.DbManager.getDatabase(subject)
        for l in file_lists:
            try:
                with open(os.getcwd() + "/Data/" + subject + '/' + location + "/data/" + l, 'r') as file:
                    data = {
                        "subject": subject,
                        "location": location,
                        "data": json.loads(file.read())
                    }
                    status = db[location].insert_one(data)
                    print(str(status.inserted_id) + "upload successful!")
                file.close()
            except FileNotFoundError as fe:
                print(fe)
                continue
            except JSONDecodeError as je:
                print("Data format Error for " + l)
                continue
        print("Upload complete.")


async def main():
    print("Data Banker Usage: --subject [Subject] --location [Location]")
    data_bank = Data_Banker()
    subject = ""
    location = ""
    command = sys.argv
    if len(sys.argv) > 0:
        for i, c in enumerate(command):
            if "--subject" in c:
                subject = command[i + 1]
            if "--location" in c:
                location = command[i + 1]

    data_bank.store_archives(subject, location)


if __name__ == "__main__":
    # loop to keep main thread running
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
