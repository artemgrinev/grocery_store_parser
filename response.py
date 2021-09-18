import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from key import key

class Response:
    def __init__(self):
        url = 'https://...'
        key = ""

    def get_soup(self):
        r = requests.get(self.url, headers={'User-Agent': UserAgent().chrome}).text
        soup = BeautifulSoup(r)
        return soup

    def get_proxy(self):
        proxy_host = "proxy.zyte.com"
        proxy_port = "8011"
        proxy_auth = self.key # Make sure to include ':' at the end
        proxies = {"https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                   "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
        r = requests.get(self.url, proxies=proxies, verify=False).text
        soup = BeautifulSoup(r)
        return soup

response = Response()
response.key = key