# -*- coding: utf-8 -*-

import requests
import os
import shutil


def get_service_status(url):
    try:
        r = requests.get(url)
        return "Running"
    except requests.ConnectionError:
        return "Not Running"

def init_unicorn_database():
    """Copy default one into user's own directory.
    """
    default_dir_name = os.path.expanduser('~/.unicorn')
    default_file_name = 'unicorn.sqlite'
    full_name = os.path.join(default_dir_name, default_file_name)
    db_src = os.path.join('/usr/share/unicorn/unicorn.sqlite')
    if os.path.exists(default_dir_name):
        if not os.path.exists(full_name):
            shutil.copy(db_src, default_dir_name)
    else:
        os.mkdir(default_dir_name)
        shutil.copy(db_src, default_dir_name)


if __name__ == "__main__":
    url = 'http://127.0.0.1:5000'
    print(get_service_status(url))
