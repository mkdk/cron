# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'music_scrapper'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

#db = MySQLdb.connect("11.50.5.0","cpses_pavWfg5xZI@localhost","pacciari12","pacciari_island1234" )

import sys
import MySQLdb
# SQL DATABASE SETTING
SQL_DB = 'newdatabase'
SQL_TABLE = 'songs_shazam' 
SQL_HOST = '127.0.0.1'
SQL_USER = 'root'
SQL_PASSWD = 'root'

#SQL_DB = 'pacciari_island1234'
#SQL_TABLE = 'songs_chart'
#SQL_HOST = '127.0.0.1'
#SQL_USER = 'pacciari_pacciari12'
#SQL_PASSWD = 'pacciari12'
#SQL_PASSWD = '$Mi@To3kE7Kp'

#SQL_DB = 'pacciari_island1234' #cpanelUsername_databaseName
#SQL_TABLE = 'songs_chart' #tablename
#SQL_HOST = 'localhost' #localhost   #127.0.0.1 107.180.58.46   209.140.42.66 11.50.5.0 cpses_pavWfg5xZI@localhost
#SQL_USER = 'pacciari_pacciari12' #cpanelUsername_databaseUsername
#SQL_PASSWD = 'pacciari12' #dbpassword
#SQL_PORT= 3306


#SQL_DB = 'island1234'
#SQL_TABLE = 'songs_chart'
#SQL_HOST = 'www.island-research.com'
#SQL_USER = 'pacciari12'
#SQL_PASSWD = 'pacciari12'
    # connect to the MySQL server
try:
   CONN = MySQLdb.connect(host=SQL_HOST,
                             user=SQL_USER,
                             passwd=SQL_PASSWD,
                             db=SQL_DB,
                             charset='utf8',use_unicode=True)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

DOWNLOAD_TIMEOUT = 2000
RETRY_TIMES=10
#DUPEFILTER_DEBUG=True
#REDIRECT_ENABLED=False
#COOKIES_ENABLED = True
# HTTPCACHE_ENABLED=True
# AJAXCRAWL_ENABLED=True
#USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"


# CONCURRENT_REQUESTS=1
# CONCURRENT_REQUESTS_PER_DOMAIN=1
# CONCURRENT_ITEMS=1
#DOWNLOAD_DELAY =1   #how many seconds you want your spider to wait to download other request

# ITEM_PIPELINES = {'tutorial.pipelines.TutorialPipeline': 300 }

DOWNLOADER_MIDDLEWARES = {
 	'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
	'tutorial.middlewares.ProxyMiddleware': 100,
}


# README
# open tutorial.middlewares.ProxyMiddleware for changing proxy server
# pay attention proxy must be good and if proxy for "https" use
# "https" in address if it "http" type http
# example http://some.address or https://some.address
# here is good service where you can find good proxy http://checkerproxy.net/
# before use some proxy check it and if it's ok continue