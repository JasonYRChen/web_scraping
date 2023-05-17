import time
import datetime
import re
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pprint import pprint


def fetch_ip(bs_root):
    """
        Based on BeautifulSoup object to yield all legit IPs
    """

    pattern = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
    bdis = bs_root.find_all('bdi')
    for bdi in bdis:
        ip = bdi.get_text()
        if pattern.match(ip):
            yield ip


def fetch_ip_location(ip):
    """
        Call api from 'ip-api' to retrieve json response
    """

    base_api = 'http://ip-api.com/json/'
    api = base_api + ip
    response = urlopen(api).read()
    info_json = json.loads(response)
    return info_json


def show_ip_info(info_json, *fields: tuple[str]):
    """
        Based on json response from 'ip-api' and designated fields to 
        retrieve information in the former. If field name in 'fields'
        is not found in 'info_json', 'Unknown' will return as the field
        value.
    """
    retrieved = {} 
    for field in fields:
        retrieved[field] = 'Unknown' \
                           if field not in info_json else info_json[field]
    string = ', '.join(f'{k}: {v}' for k, v in retrieved.items())
    return string 


def revisor_ip_location(base_url, sub_url, elements_per_page, *fields):
    """
        Return IP information of all revisors with IP address in selected 
        Wiki page.
    """

    limit = f'&limit={elements_per_page}'
    page = 1
    start = time.time()
    searched_ip = set()

    while query_url := base_url + sub_url + limit:
        print(f'page: {page}')
        bs_root = bs(urlopen(query_url), 'html.parser')

        for ip in fetch_ip(bs_root):
            if ip not in searched_ip:
                searched_ip.add(ip)
                info_json = fetch_ip_location(ip)
                ip_info = show_ip_info(info_json, *fields)
                print(f'  --{ip_info}')

        next_page = bs_root.find(attrs={'class': 'mw-nextlink'})
        if next_page.name == 'a':
            sub_url = next_page.attrs['href']
        else:
            base_url = sub_url = limit = ''

        page += 1

    lapses = time.time() - start
    lapses = datetime.timedelta(seconds=lapses)
    print(f'Lapse {lapses}, {len(searched_ip)} IP were found.')


base_url = 'https://en.wikipedia.org'
sub_url = '/w/index.php?title=Python_(programming_language)&action=history'
revisor_ip_location(base_url, sub_url, 5000, 'query', 'country')
