# !/usr/bin/python
# _*_ codding:utf-8 _*_

import os
import re
import random
import subprocess
from subprocess import PIPE, Popen


def get_proxy():
    home = os.path.abspath(os.path.dirname(__file__))
    print home
    if os.path.exists(os.path.join(home,'proxy.txt')):
        os.system('rm %s' % os.path.join(home, 'proxy.txt'))
        print('the old proxy.txt was deleted')
    os.system(os.path.join(home, 'sh/wget.sh'))
    proxy = []
    path = os.path.join(home, 'proxy.txt')
    print (path)
    with open(path) as f:
        for e, line in enumerate(f.readlines()):
            if e > 4:
                line = line.split(' ')
                if "US-A" or "DE-A" or "CN-A" in line[1]:
                    proxy.append(line[0])
            if e == 80:
                break
    proxy = second_filter(proxy)
    with open(os.path.join(home,'proxy.txt'), 'w') as w:
        for i in proxy:
            w.write(i+'\n')
    print('proxy.txt has been download and prepared')


def second_filter(proxy):
    best = []
    for i in proxy:
        p = subprocess.Popen('curl -x http://%s -L https://myip.ht' % i, shell=True, stdout=PIPE, stderr=PIPE)
        p.wait()
        if '<!DOCTYPE html><html><head><title>What\'s My IP Address?</title>' in p.communicate():
            print("good %s" % i)
            best.append(i)
    return best



def change_proxy(spider, proxy):
    middl = open(os.path.join(spider, 'tutorial', 'middlewares.py')).read()
    with open(os.path.join(spider,'tutorial','middlewares.py'), 'w') as f:
        with open(proxy, ) as s:
            proxy_c = [i for i in s.readlines()]
        p = re.findall(r'\d+.\d+.\d+.\d+.\d+', middl)
        random_proxy = proxy_c[random.randint(0, (len(proxy_c)-1))].replace('\n', '')
        print p, random_proxy
        middl = middl.replace(p[0], random_proxy)
        f.write(middl)



if __name__ == "__main__":
    get_proxy()