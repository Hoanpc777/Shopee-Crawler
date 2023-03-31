import random
from seleniumwire import webdriver as wiredriver
from seleniumwire.utils import decode
import json
# Chrome
from selenium.webdriver.chrome.service import Service as chrome_Service
from selenium.webdriver.chrome.options import Options as chrome_Options
#Firefox
from selenium.webdriver.firefox.service import Service as ff_Service
from selenium.webdriver.firefox.options import Options as ff_Options
#Edge
from selenium.webdriver.edge.service import Service as edge_Service
from selenium.webdriver.edge.options import Options as edge_Options

# Run browser
def browser():
    # # Random to choose browser
    # """
    # 1-Firefox 2-Chrome 3-Edge
    # """
    ran = random.randint(1, 3)
    if ran == 1: driver = firefox_browser()
    elif ran == 2: driver = chrome_browser()
    elif ran == 3: driver = edge_browser()
    # driver = firefox_browser()
    return driver
    
# Run firefox
def firefox_browser():
    options = ff_Options()
    options.add_argument('--headless') # run in headless mode (without GUI)
    service = ff_Service('/path/to/geckodriver',log_path='nul') # path to chromedriver executable
    driver = wiredriver.Firefox(service=service, options=options)
    return driver

# Run chrome
def chrome_browser():
    options = chrome_Options()
    options.add_argument('--headless') # run in headless mode (without GUI)
    service = chrome_Service('/path/to/chromedriver') # path to chromedriver executable
    driver = wiredriver.Chrome(service=service, options=options)
    return driver

# run edge browser
def edge_browser():
    options = edge_Options()
    options.add_argument('--headless') # run in headless mode (without GUI)
    service = edge_Service('/path/to/msedgedriver') # path to chromedriver executable
    driver = wiredriver.Edge(service=service, options=options)
    return driver

# run json data
def get_json_data(url, api):
    driver = browser()
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