#!/usr/bin/python
import asyncio
import json
import os
import sys
import re
from time import sleep
from urllib.request import urlopen
from PIL import Image
from ibm_cloud_sdk_core import ApiException
from ibm_watson.natural_language_understanding_v1 import EntitiesOptions, RelationsOptions, Features, KeywordsOptions
from pytesseract import pytesseract
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from classes.archiver import Archiver

class Google_Scraper(Archiver):
    def __init__(self):
        super().__init__()

    def google_scraper(self, driver, search_term, domain_region=""):
        driver.get(url="https://google.com" + domain_region)
        sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(search_term).send_keys(Keys.RETURN).perform()
        sleep(2)
        hrefs = []

        while True:
            found_pages = [driver.find_elements_by_xpath(".//div[contains(@class, 'rc')]")]
            for l in found_pages[0]:
                hrefs += [l.find_element_by_xpath(".//a").get_attribute("href")]

            try:
                next = driver.find_elements_by_xpath(".//div[contains(@id, 'foot')]//td")[-1]
                driver.get(next.find_element_by_xpath(".//a").get_attribute("href"))
            except NoSuchElementException as nse:
                print(nse)
                break
            sleep(2)

        # start going through pages
        for r in hrefs:
            self.scraper_page(driver, r)
        print("Search scrape complete!")

    def scrape_page(self, driver, url):
        driver.get(url)
        body = driver.find_element_by_xpath("//body")
        html = driver.find_element_by_xpath("//html")
        extracted_text = body.text
        images = body.find_elements_by_xpath("//img")
        title = re.findall("([^/]+)(?=[^/]*/?$)", url)[0]
        title = re.sub(r"[^a-zA-Z0-9]", "", title)
        keywords_js = []
        relations_js = []
        entities_js = []

        if len(extracted_text) > 0:
            entities_js += [json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                entities=EntitiesOptions(sentiment=True))).get_result())]
            relations_js += [json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                relations=RelationsOptions())).get_result())]
            keywords_js += [json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                keywords=KeywordsOptions(sentiment=True, emotion=True))).get_result())]
            data_set = {
                "document": title,
                "url": url,
                "entities": entities_js,
                "relations": relations_js,
                "keywords": keywords_js
            }
            filepath = os.getcwd() + "/Data"
            # try:
            #     os.makedirs(filepath)
            #     print("New Directory ", filepath, " Created ")
            # except FileExistsError:
            #     print("Directory ", filepath, " already exists")

            fileOut = open(filepath + '/' + title.strip('.') + ".json", "w")
            fileOut.write(json.dumps(data_set))
            fileOut.close()
            print(title + " extraction complete!")

        if len(images) > 0:
            for i in images:
                try:
                    img = Image.open(urlopen(i.get_attribute("src")))
                    img.save("images/" + driver.find_element_by_xpath("//img").get_attribute("src").split("/")[-1])
                    extracted_text = pytesseract.image_to_string(Image.open(urlopen(i.get_attribute("src"))))
                    sleep(3)
                    entities_js += [json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                        entities=EntitiesOptions(sentiment=True))).get_result())]
                    relations_js += [json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                        relations=RelationsOptions())).get_result())]
                    keywords_js += [json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                        keywords=KeywordsOptions(sentiment=True, emotion=True))).get_result())]
                except ApiException as ex:
                    print("Method failed with status code " + str(ex.code) + ": " + ex.message)
                except OSError as OSe:
                    print("Method failed with status code " + str(OSe))

        data_set = {
            "document": title + "_IMAGES_DATA",
            "url": url,
            "entities": entities_js,
            "relations": relations_js,
            "keywords": keywords_js
        }

        filepath = os.getcwd() + "/Data"
        fileOut = open(filepath + '/' + title.strip('.') + ".json", "w")
        fileOut.write(json.dumps(data_set))
        fileOut.close()
        print(title + " extraction complete!")

async def main():
    print("Google Scrape Usage: --search ['search term in quotes'] --region [.au]")
    scraper = Google_Scraper()
    driver = scraper.initChromeDriver(False)
    search = ""
    region = ""
    command = sys.argv
    if len(sys.argv) > 0:
        for i, c in enumerate(command):
            if "--search" in c:
                search = command[i+1]
            if "--region" in c:
                region = command[i+1]
    scraper.google_scraper(driver, search, region)


if __name__ == "__main__":
    # loop to keep main thread running
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    #toDO implament fact checker to subject search finder to compare the likelyhood of truth or not truth