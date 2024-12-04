#!/usr/bin/python

from __future__ import print_function
import requests
import re
import time
import random

# Configuration minimale en cas d'absence de config.py
class ConfigClass:
    MAX_DEPTH = 10  # Niveau maximum de profondeur
    MIN_DEPTH = 3   # Niveau minimum de profondeur
    MAX_WAIT = 10   # Temps max entre les requêtes
    MIN_WAIT = 5    # Temps min entre les requêtes
    DEBUG = False   # Activer/désactiver les messages de débogage
    ROOT_URLS = [
        "https://www.example.com"
    ]
    blacklist = [
        'facebook.com',
        'pinterest.com'
    ]
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

config = ConfigClass

# Liste des proxies
proxies_list = [
    'http://8.218.117.116:8080',
    'http://72.10.160.172:8080',
    'http://95.154.20.113:3128',
    'http://202.142.145.179:8080',
    'http://89.221.215.128:1080',
    'http://41.74.91.244:8080',
    'http://68.178.168.41:3128',
    'http://93.93.246.218:1080'
]

class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    NONE = '\033[0m'

def debug_print(message, color=Colors.NONE):
    if config.DEBUG:
        print(color + message + Colors.NONE)

def hr_bytes(bytes_, suffix='B', si=False):
    bits = 1024.0 if si else 1000.0
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes_) < bits:
            return "{:.1f}{}{}".format(bytes_, unit, suffix)
        bytes_ /= bits
    return "{:.1f}{}{}".format(bytes_, 'Y', suffix)

def get_random_proxy():
    """Sélectionne un proxy aléatoire dans la liste."""
    return random.choice(proxies_list)

def do_request(url):
    global data_meter
    global good_requests
    global bad_requests

    debug_print("Requesting page... {}".format(url))

    headers = {'user-agent': config.USER_AGENT}
    proxy = get_random_proxy()  # Obtenez un proxy aléatoire

    try:
        r = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=5)
    except Exception as e:
        debug_print(f"Proxy failed: {proxy}. Error: {e}", Colors.RED)
        bad_requests += 1
        return False

    page_size = len(r.content)
    data_meter += page_size

    debug_print("Page size: {}".format(hr_bytes(page_size)))
    debug_print("Data meter: {}".format(hr_bytes(data_meter)))

    status = r.status_code

    if status != 200:
        bad_requests += 1
        debug_print("Response status: {}".format(r.status_code), Colors.RED)
        if status == 429:
            debug_print("Too many requests... sleeping longer...")
            config.MIN_WAIT += 10
            config.MAX_WAIT += 10
    else:
        good_requests += 1

    debug_print("Good requests: {}".format(good_requests))
    debug_print("Bad requests: {}".format(bad_requests))

    return r

def get_links(page):
    pattern = r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, str(page.content))
    valid_links = [link for link in links if not any(b in link for b in config.blacklist)]
    return valid_links

def recursive_browse(url, depth):
    debug_print("Recursively browsing [{}] ~~~ [depth = {}]".format(url, depth))
    if not depth:
        do_request(url)
        return
    else:
        page = do_request(url)
        if not page:
            debug_print("Stopping and blacklisting: page error".format(url), Colors.YELLOW)
            config.blacklist.append(url)
            return

        debug_print("Scraping page for links".format(url))
        valid_links = get_links(page)
        debug_print("Found {} valid links".format(len(valid_links)))

        if not valid_links:
            debug_print("Stopping and blacklisting: no links".format(url), Colors.YELLOW)
            config.blacklist.append(url)
            return

        sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
        debug_print("Pausing for {} seconds...".format(sleep_time))
        time.sleep(sleep_time)

        recursive_browse(random.choice(valid_links), depth - 1)

if __name__ == "__main__":
    data_meter = 0
    good_requests = 0
    bad_requests = 0

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Traffic generator started")
    print("Diving between 3 and {} links deep into {} root URLs,".format(
        config.MAX_DEPTH, len(config.ROOT_URLS)))
    print("Waiting between {} and {} seconds between requests.".format(
        config.MIN_WAIT, config.MAX_WAIT))
    print("This script will run indefinitely. Ctrl+C to stop.")

    while True:
        random_url = random.choice(config.ROOT_URLS)
        depth = random.choice(range(config.MIN_DEPTH, config.MAX_DEPTH))
        recursive_browse(random_url, depth)
