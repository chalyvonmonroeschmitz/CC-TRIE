#!/usr/bin/python
import os
import sys
import time
from time import sleep
from pynput.keyboard import Key, Controller
# Load webdriver
from selenium import webdriver
# Load proxy option
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.webdriver import WebDriver

class Scraper:
    def __init__(self):
        self.role = "Template"
        self.key = {}
        self.driver = None

    def load_edge_driver(self, webdriver):
        # Set the path to the Edge WebDriver executable
        edge_driver_path = '.lib/msedgedriver.exe'  # Update this path to your Edge WebDriver executable

        # Set up Edge options
        edge_options = Options()
        edge_options.use_chromium = True

        # Initialize the Edge WebDriver
        service = Service(".lib/msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=edge_options)
        return driver

    def initChromeDriver(self, headless=False):
        driver = webdriver.Chrome
        chrome_options = webdriver.ChromeOptions()
        # Configure Proxy Option
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        # Proxy IP & Port
        # proxy.http_proxy = self.security_manager.key_service.config['proxy']['http_proxy']
        # proxy.ssl_proxy = self.security_manager.key_service.config['proxy']['ssl_proxy']
        # Configure capabilities and proxy whitelist
        chrome_options.add_argument("--whitelisted-ips='0.0.0.0'")
        capabilities = webdriver.DesiredCapabilities.CHROME
        # proxy.to_capabilities(capabilities)
        if headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        # cookie store options
        # chrome_options.add_argument("--user-data-dir=sessions")
        # merge desired with options

        if sys.platform == 'win32':
            driver = webdriver.Chrome()
            # driver = webdriver.Remote("http://192.168.58.1:4444", options=chrome_options)
            # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=chrome_options, desired_capabilities=capabilities)

        elif sys.platform == 'linux':
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options, desired_capabilities=capabilities)
        return driver

    def enter_proxy_login(self, driver: webdriver.Chrome, username: str, password: str):
        # send focus to window
        keyboard = Controller()
        # driver.maximize_window()
        driver.switch_to.window(driver.window_handles[0])

        print("entering proxy ...")
        proxy_username = username
        proxy_password = password

        # send keypresses to credential box
        keyboard.type(proxy_username)
        sleep(2)
        keyboard.press(Key.tab)
        keyboard.type(proxy_password)
        sleep(2)
        keyboard.press(Key.enter)
        sleep(2)

    @staticmethod
    def start_session(self, driver:  webdriver.Chrome, socialnetwork_name):
        pass

    @staticmethod
    def logon(self, driver:  webdriver.Chrome, socialnetwork_name):
        pass

    @staticmethod
    async def get_key(self):
        pass

    @staticmethod
    async def get_session(self, driver: webdriver.Chrome):
        pass
