# -*- coding: utf-8 -*-
import subprocess
import scrapy
import json
import pprint
import os
import random
from tutorial.mymusic import MusicItem
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from urlparse import urlparse
from scrapy.utils.response import open_in_browser
from tutorial.settings import *
import sys
import time
from selenium import webdriver
import csv
from xml.dom.minidom import parse
import xml.dom.minidom
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import spotipy
import spotipy.util as util
import MySQLdb
from MySQLdb import escape_string
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from datetime import date
#import msvcrt


class MusicSpider(scrapy.Spider):

    name = "music"
    global lastthursdate
    lastthursdate=""
    start_urls=["http://www.shazam.com"]

    todays_date=datetime.datetime.today().weekday()

    global x
    x=CONN.cursor()

    def parse(self, response):
        
                
        sel=Selector(response)


        # ########################################################3

        # # #shazam mobile proxy
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[0].strip())!=0 and count!=0 and row[0].strip()=="Shazam Mobile Proxy URL":
                    links.append(row)
                else:
                    count=count+1

        now = datetime.date.today()
        date=now.strftime("%Y%m%d")

        for l in links:
            req = Request(l[4].strip()+date+l[6],meta={'source': l[0].strip(),
                                                       'chart_type': l[1],
                                                       'chart': l[2],
                                                       'chart_name': l[3],
                                                       'state': l[10]},
                          callback=self.each_detail)
            yield req
            #self.driver.quit()

    def each_detail(self,response):
        #open_in_browser(response)

        sel=Selector(response)

        source=response.meta['source']
        # spotify charts website

        #shazam mobile proxy

        if source=="Shazam Mobile Proxy URL":
            chart_name=response.meta['chart_name']
            chart_type=response.meta['chart_type']

            chart_name="".join(chart_name)+" (US)"
            f=open("temp.json",'w+b')
            f.write(response.body)
            f.close()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")

            with open("temp.json") as json_file:
                json_data = json.load(json_file)
                total_results=json_data["chart"]

                rank=1

                for t in total_results:
                    song=t["heading"]["title"]
                    artist=t["heading"]["subtitle"]

                    try:
                        sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s')" % ("songs_shazam",
                  escape_string("".join(artist).encode('utf-8').strip()),
                  escape_string("".join(song).encode('utf-8').strip()),
                  escape_string("US Local"),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string(str(rank)),
                  now,
                  )

                        global x
                        if x.execute(sql):
                            var=1
                            #print "item Inserted"
                        else:
                            print "Something wrong"

                    except Exception,e:
                        raise e
                        pass

                    rank=rank+1
        CONN.commit()
