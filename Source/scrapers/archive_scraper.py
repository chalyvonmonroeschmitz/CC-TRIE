#!/usr/bin/python
import asyncio
import os
import sys
import json
from PIL import Image
from urllib.request import urlopen
import pytesseract
from time import sleep
from ibm_cloud_sdk_core import ApiException
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EntitiesOptions, RelationsOptions, \
    KeywordsOptions
from os import walk
from pdf2image import convert_from_path, convert_from_bytes
from Source.scrapers import Archiver
import pandas as pd


class Archive_Scraper(Archiver):
    def __init__(self):
        super().__init__()

    def extract_from_file(self, subject, location, document, filename):
        print("Processing " + filename + "....")
        filepath = os.getcwd() + "/Data/" + subject + '/' + location
        try:
            if ".pdf" == filename[-4:]:
                convert_from_path(filepath + '/' + filename, output_folder=filepath + "/images", fmt="jpeg")
                print("PDF pages extracted to ./images directory")
            elif ".xlsx" == filename[-5:]:
                data = pd.read_excel(filepath + '/' + filename)
                fileOut = open(filepath + "/data/" + document + ".json", 'w')
                fileOut.write(data.to_json())
                fileOut.close()
        except Exception as ex:
            print(ex)
        print(filename + " extraction complete")
        return True

    def extract_from_images(self, subject, location):
        entities_js = []
        relations_js = []
        keywords_js = []
        files = []
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + '/Data/' + subject + '/' + location + "/images"):
            files.extend(filenames)
            break

        for i in files:
            try:
                document = i[:str(i).find('.')]
                print("Extracting image " + document + "...")
                # check if already processed
                if os.path.isfile(os.getcwd() + "/Data/" + subject + '/' + location + '/' + "/data/" + document[:str(
                        document).find('.')] + ".json"):
                    print("Image already extracted, continuing")
                    continue

                img = Image.open(os.getcwd() + "/Data/" + subject + '/' + location + "/images/" + i)
                extracted_text = pytesseract.image_to_string(img)
                sleep(3)
                entities_js = json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                    entities=EntitiesOptions(sentiment=True))).get_result())
                relations_js=json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                    relations=RelationsOptions())).get_result())
                keywords_js=json.dumps(self.watson_nlu.analyze(text=extracted_text, features=Features(
                    keywords=KeywordsOptions(sentiment=True, emotion=True))).get_result())
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            except OSError as OSe:
                print("Method failed with status code " + str(OSe))

            data_set = {
                "title": subject,
                "location": location,
                "filename": document,
                "entities": entities_js,
                "relations": relations_js,
                "keywords": keywords_js
            }
            fileOut = open(os.getcwd() + "/Data/" + subject + '/' + location + '/' + "/data/" + document[:str(document).find('.')] + ".json", "w")
            fileOut.write(json.dumps(data_set, indent=2))
            fileOut.close()
            print(document + " complete!")


    def scrape_archive(self, driver, url):
        driver.get(url)
        text_list = []
        text_links = []
        for text in driver.find_elements_by_xpath(".//table/tbody/tr/td[2]/center[2]/table//a"):
            text_list += [text.text]
        for l in driver.find_elements_by_xpath(".//table/tbody/tr/td[2]/center[2]/table//a"):
            try:
                text_links += [l.get_attribute("href")]
            except Exception as e:
                text_links += "None"
        ship_links = [text_list, text_links]
        for l in zip(ship_links[1], ship_links[0]):
            if "None" not in l[0]:
                driver.get(l[0])
                images = driver.find_elements_by_xpath("//img")
                extracted_text = driver.find_element_by_xpath("//html").text
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
                        "registry_name": l[1],
                        "entities": entities_js,
                        "relations": relations_js,
                        "keywords": keywords_js
                    }

                    fileOut = open("Data/Passengers/" + l[0][-1] + ".json", "w+")
                    fileOut.write(json.dumps(data_set))
                    fileOut.close()
                    print(data_set)

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
                    "registry_name": l[1],
                    "entities": entities_js,
                    "relations": relations_js,
                    "keywords": keywords_js
                }

                fileOut = open("Data/Passengers/" + l[1][0:16] + ".json", "w")
                fileOut.write(json.dumps(data_set))
                fileOut.close()
                print(data_set)


async def main():
    subject = ""
    location = ""
    command = sys.argv
    scraper = Archive_Scraper()
    if len(sys.argv) > 0:
        for i, c in enumerate(command):
            if "--subject" in c:
                subject = command[i+1]
            if "--location" in c:
                location = command[i+1]
    else:
        print("no parameters give: --subject [name] --location [place]")
        exit(1)
    files = []
    for (dirpath, dirnames, filenames) in walk(os.getcwd() + '/Data/' + subject + '/' + location):
        files.extend(filenames)
        break
    # # process files
    # for file in files:
    #     document = file[:str(file).find('.')]
    #     scraper.extract_from_file(subject, location, document, file)

    # process images
    for file in files:
        document = file[:str(file).find('.')]
        scraper.extract_from_images(subject, location)

if __name__ == "__main__":
    # loop to keep main thread running
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
