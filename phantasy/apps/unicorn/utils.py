# -*- coding: utf-8 -*-

import requests


def get_service_status(url):
    try:
        r = requests.get(url)
        return "Running"
    except requests.ConnectionError:
        return "Not Running"


if __name__ == "__main__":
    url = 'http://127.0.0.1:5000'
    print(get_service_status(url))
