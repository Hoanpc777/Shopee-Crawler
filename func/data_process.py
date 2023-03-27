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
from .character_process import flat_dict as flat_dict

# Run mô phỏng chrome
def browser():
  chrome_options = Options()
  chrome_options.add_argument('--headless') # run Chrome in headless mode (without GUI)
  service = Service('/path/to/chromedriver') # path to chromedriver executable
  driver = wiredriver.Chrome(service=service, options=chrome_options)

  # driver = webdriver.Firefox()#webdriver.Chrome(options=chrome_options)
  return driver

# Get detail infor items
def get_in4_item(shopid, itemid):
  item_url = f"https://shopee.vn/api/v4/item/get?itemid={itemid}&shopid={shopid}"

  payload={
  }
  headers = {
    'authority': 'shopee.vn',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-api-source': 'pc',
    'x-kl-ajax-request': 'Ajax_Request',
    'x-requested-with': 'XMLHttpRequest',
    'x-shopee-language': 'vi'
  }

  response = requests.request("GET", item_url, headers=headers, data=payload)

  item_raw=response.json()
  product_data=pd.json_normalize(item_raw['data'])
  inf = product_data[['shopid','itemid','brand','price','stock','discount','historical_sold','sold','description','item_rating.rating_star','images','categories','shop_vouchers','global_sold']]
  inf = pd.concat([inf,flat_dict(inf['categories'],'display_name')],axis=1)
  return inf

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