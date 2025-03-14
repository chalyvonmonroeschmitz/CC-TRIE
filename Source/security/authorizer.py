#!/usr/bin/python
from datetime import time
import os
import random
from os import walk
import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection as mongoCollection
from pymongo.database import Database
from selenium import webdriver
import requests


class DataManager:
    def __init__(self, connection_string : str = "not configured"):
        self.client: MongoClient = None
        self.db: Database = None
        self.collection: mongoCollection = None
        self.status = "offline"
        self.connection_string = connection_string
        self.client = MongoClient(self.connection_string)

    def getDatabase(self, name: str):
        self.db = self.client.get_database(name)
        self.client.close()
        return self.db

    def getCollection(self, database : str, collection: str):
        db = self.getDatabase(database)
        self.collection = db.get_collection(collection)
        self.client.close()
        return self.collection

    def status(self):
        return self.status


class Authorizer:
    def __init__(self):
        self.path = os.getcwd()
        self.account = {}
        self.DbManager: DataManager = DataManager()
        self.Social_Network_Name = ""
        self.key_service: Messenger = Messenger()

    def set_connection_id(self, username: str, password: str, connection_url: str):
        self.DbManager = DataManager(connection_url %(username, password))

    def get_dbUser(self, username: str):
        user = username
        if user:
            return user
        else:
            print("user does not exist")
            return False

    def set_key_service(self, key_object: Messenger):
        self.key_service = key_object
        return self.key_service

    def getRandomAccount(self, db_user: dict, db_name, connection_url: str, social_network):
        self.set_connection_id(db_user['username'], db_user['password'], connection_url)
        db = self.DbManager.getDatabase(db_name)

        while True:
            try:
                creds_list = db[social_network].find()
                user = db[social_network].find().limit(-1).skip(random.randint(1, creds_list.count())).next()
                if user['Status'] == "Active" or user['Status'] == "Unconfirmed":
                    return user
            except Exception as e:
                print("no available accounts for use")
                return False

    def load_accounts(self, social_network: str):
        self.Social_Network_Name = social_network
        cred_config = self.key_service.config_dictionary
        cred_user = self.key_service.config['cloud.mongodb']['credential_manager']
        self.set_connection_id(cred_user['username'], cred_user['password'], cred_config['MONGO_SERVER'])
        db = self.DbManager.getDatabase("Security")
        doc = db.get_collection(social_network)
        accounts = []
        # re.emails = f"[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+"
        # re.password = f"(?<=.com:).\w*"

        f = []
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + "/.resx/", topdown=True):
            dirnames.clear()
            f.extend(filenames)

        creds = {}

        for filename in f:
            if "facebook" in str(filename).lower() and social_network in str(filename).lower():
                with open(self.path + "/.resx/" + filename) as data:
                    for line in data.readlines():
                        accounts += [line]

                for l in accounts:
                    sections = str(l).split("|")
                    username = sections[0]
                    password = sections[1]
                    cookies = sections[2]
                    uids = sections[0]
                    status = "Unconfirmed"

                    creds += ({
                        "Username": username,
                        "Password": password,
                        "Cookie": cookies,
                        "Uid": uids,
                        "Dob": "None",
                        "Email": "None",
                        "Email_Pass": "None",
                        "User_Agent": "None",
                        "Status": status,
                        "Social_Network": social_network
                    })

                    for k, v in zip(creds.keys(), creds.values()):
                        if k == "Username":
                            if doc.find_one({"Username": v}):
                                break

                        x = self.DbManager.db[social_network].insert_one(creds)
                        print(x.inserted_id)

            elif "twitter" in str(filename).lower() and social_network.lower() in str(filename).lower():
                with open(self.path + "/.resx/" + filename) as data:
                    for line in data.readlines():
                        accounts += [line]

                for l in accounts:
                    try:
                        sections = str(l).split(":")
                        username = sections[0].strip()
                        email = sections[1].strip()
                        password = sections[2].strip()
                        status = "Unconfirmed"
                    except Exception as e:
                        print(e)

                    creds = {
                        "Username": username,
                        "Password": password,
                        "Email": email,
                        "Status": status,
                        "Social_Network": social_network
                    }
                    if doc.find_one({"Username": creds['Username']}):
                        break

                    x = self.DbManager.db[social_network].insert_one(creds)
                    print(x.inserted_id)

    def update_account_status(self, account_id: str, status: str, database: str, role: str, network_collection: str):
        try:
            cloud_server = self.key_service.config['cloud.mongodb']
            db_string = cloud_server['connection_url']
            self.set_connection_id(cloud_server[role]['username'], cloud_server[role]['password'], db_string)
            collection: mongoCollection = self.DbManager.getDatabase(database)[network_collection]
            status = collection.update_one({"Username": account_id},  {"$set": {"Status": status}})
            print(status)
            return True
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False

    def get_jobs(self, type=None):
        print("getting available or assigned jobs")
        self.set_connection_id(self.config['cloud.mongodb']['job_manager']['username'], self.config['cloud.mongodb']['job_manager']['password'])
        jobset = []
        try:
            collection: mongoCollection = self.DbManager.getCollection("automadb", "jobs")
            for jobs in collection.find({"job_type": type}):
                if jobs['completed'] == "false":
                    jobset += [jobs]
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False
        return jobset

    def get_accound_by_id(self, id: str):
        self.set_connection_id(self.config_dictionary['CRED_USER'], self.config_dictionary['CRED_PASSWORD'])
        self.DbManager.init()
        creds: mongoCollection = self.DbManager.getCollection("Security", self.Social_Network_Name)
        account = creds.find_one({"Username": id})
        if account:
            return account
        else:
            return False

    def setSocialNetworkName(self, name: str):
        self.Social_Network_Name = name

    def getProxies(self):
        # setup api request handler
        headers = {
            'X-Hola-Auth': '<proxy>',
        }
        params = (
            ('customer', '<username>'),
            ('zone', 'static'),
            ('details', '1')
        )
        api_method = "/api/zone/ips"
        response = requests.get(f"https://proxy-provider-{api_method}", headers=headers, params=params).json()
        return response

    def createProxies(self):
        return

    def scroll_down(self, driver: webdriver.Chrome):
        # Get scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            try:
                # Scroll down to the bottom.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load the page.
                time.sleep(2)
                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

                # limit our coverage
                try:
                    posts = driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
                    year = str(posts[len(posts) - 1].find_element_by_xpath(".//span[@class='timestampContent']").text).split(" ")[2]
                    if int(year) < 2019:
                        break
                except Exception as e:
                    continue

            except Exception as e:
                return False
        return True


def main():
    print("")


if __name__ == "__main__":
    main()
