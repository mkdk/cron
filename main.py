# !/usr/bin/python
# _*_ codding:utf-8 _*_


import os
import sys
from time import sleep
from proxy_set import change_proxy

HOME = os.path.abspath(os.path.dirname(__file__))
proxy = os.path.join(HOME, 'proxy.txt')


def cronic(proxy):
    os.system(os.path.join(HOME, 'sh/local_viral_scrape.sh'))
    os.system(os.path.join(HOME, 'sh/local_sans_viral_scrape.sh'))
    os.system('python %s' % os.path.join(HOME, 'proxychecker.py'))
    change_proxy(os.path.join(HOME, 'local_shazam_us_local'), proxy)
    os.system(os.path.join(HOME, 'sh/local_shazam_us_local.sh'))
    # os.system('python %s' % os.path.join(HOME, 'proxychecker.py'))
    print('wait........')
    sleep(5)
    change_proxy(os.path.join(HOME, 'local_shazam_us_localext'), proxy)
    os.system(os.path.join(HOME, 'sh/local_shazam_us_localext.sh'))
    sys.exit()


cronic(proxy)
