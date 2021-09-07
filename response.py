import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

class GetSoup:
    url = 'https://...'
        
    def get_soup(self):
        code = requests.get(self.url, headers={'User-Agent': UserAgent().chrome}).status_code
        print(code)
        if code != 429:
            r = requests.get(self.url, headers={'User-Agent': UserAgent().chrome}).text
            soup = BeautifulSoup(r)
        else:
            try:
                proxy = self.get_proxy()
                proxies = {"http": proxy, "https": proxy}
                r = requests.get(self.url, headers={'User-Agent': UserAgent().chrome}, proxies = proxies).text
                soup = BeautifulSoup(r)
            except:
                print('conection error')
        return soup
    


    def get_proxy(self):
        print('propxy')
        url = 'https://hidemy.name/ru/proxy-list/?country=AFAXALADAOARAMAUATAZBDBYBZBJBTBOBABWBRBGBFBIKHCMCACVTDCLCNCOCGCDCRCIHRCWCYCZDKDMDOECEGGQEEETFIFRGMGEDEGHGRGTGNGYHNHKHUINIDIRIQIEILITJMJPKZKEKRKGLALVLBLSLRLYLTMOMKMGMWMYMVMLMTMQMRMUMXMDMNMEMZMMNANPNLNCNZNINENGNOPKPSPAPGPYPEPHPLPTPRRORURWMFWSSARSSCSLSGSKSISOZASSESSDSZSECHSYTWTJTZTHTLTGTRUGUAAEGBUSUYUZVEVNVGVIZMZW&type=hs#list'
        r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
        soup = BeautifulSoup(r)
        tbody = soup.find('tbody').find_all('tr')
        proxy_list = []
        for tr in tbody:
            l = []
            for td in tr.find_all('td'):
                l.append(td.text)
            port = f'http://{l[0]}:{l[1]}'
            proxy_list.append(port)
        return random.choice(proxy_list)

response = GetSoup()