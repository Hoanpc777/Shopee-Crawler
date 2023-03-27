from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wiredriver
from seleniumwire.utils import decode
import json
import pandas as pd
import requests
import numpy as np
import datetime, time
import os

# Run mô phỏng chrome
def browser():
  chrome_options = Options()
  chrome_options.add_argument('--headless') # run Chrome in headless mode (without GUI)
  service = Service('/path/to/chromedriver') # path to chromedriver executable
  driver = wiredriver.Chrome(service=service, options=chrome_options)

  # driver = webdriver.Firefox()#webdriver.Chrome(options=chrome_options)
  return driver

def get_json_data(url, api):
    chrome_options = Options()
    chrome_options.add_argument('--headless') # run Chrome in headless mode (without GUI)
    service = Service('/path/to/chromedriver') # path to chromedriver executable
    driver = wiredriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    for request in driver.requests:
        if request.response:
            if request.url.startswith(api):
                response = request.response
                # body = decode(response.body, response.headers.get('Content-Encoding', 'Identify'))
                content_encoding = response.headers.get('Content-Encoding')
                if content_encoding is None:
                    content_encoding = 'identity'
                body = decode(response.body, content_encoding)
                decoded_body = body.decode('utf8')
                json_data = json.loads(decoded_body)
                return json_data