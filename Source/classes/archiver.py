#!/usr/bin/python
import asyncio
import os
import sys
import pytesseract
from classes.scraper import Scraper
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# If you don't have tesseract executable in your PATH, include the following:


class Archiver(Scraper):
    def __init__(self):
        self.init()

    def init(self):
        # watson image visualizer
        # watson nlu
        self.nlu_authenticator = IAMAuthenticator('ApiKey-7671f28d-699f-48af-a12a-79935c9cee6e')
        self.watson_nlu = NaturalLanguageUnderstandingV1(
            version='2020-08-01',
            authenticator=self.nlu_authenticator
        )
        self.watson_nlu.set_service_url("https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/b3650a84-8568-4371-b4ff-ea06c2d0ea35")


async def main():
    print("Archiver")


if __name__ == "__main__":
    # loop to keep main thread running
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
