# -*- coding: utf-8 -*-
import scrapy
import json
import pprint
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
        
        #Spotify charts viral
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[3].strip()=="Viral4":
                    links.append(row)
                else:
                    count=count+1
        
        for l in links:
            yield Request(l[4],meta={'source':l[3].strip(),'chart_type':l[1].strip(),'chart_name':l[3],'chart_name_2':l[10]},callback=self.each_detail)
        
        # SPOTIFY CHARTS WEBSITE

        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="Spotify Charts Website":
                    links.append(row)
                else:
                    count=count+1

        

        for l in links:
            yield Request(l[4],meta={'source':l[0].strip(),'chart_type':l[1].strip(),'chart_name':l[3],'chart_name_2':l[10]},callback=self.each_detail)
        
        
        # SHAZAM

        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="Shazam.com":
                    links.append(row)
                else:
                    count=count+1
            
        for l in links:
            yield Request(l[4],meta={'source':l[0].strip(),'chart_type':l[1].strip()}, callback=self.each_detail)

        # ##################################################
        #ITUNES 
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="iTunes RSS":
                    links.append(row)
                else:
                    count=count+1
        
        #chart => song or album
        for l in links:
            yield Request(l[4],meta={'source':l[0].strip(),'chart_type':l[1],'chart':l[2].strip(),'chart_name':l[3],'chart_name_2':l[10]},callback=self.each_detail)
        
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
            yield Request(l[4].strip()+date+l[6],meta={'source':l[0].strip(),'chart_type':l[1],'chart':l[2],'chart_name':l[3]},callback=self.each_detail)

        # ###############################################################
        # # Twitter 

        yield Request("http://realtime.billboard.com/proxy/?chart=3&chartName=Emerging",meta={'source':"Realtime.Billboard.com",'chart_type':"Twitter",'chart':"Song",'chart_name':"Emerging Artists"},callback=self.each_detail)

        # ################################################################

        # #Hype Machine

        yield Request("http://hypem.com/popular/noremix/10",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/9",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/8",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/7",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/6",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/5",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/4",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/3",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/2",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        yield Request("http://hypem.com/popular/noremix/1",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        
        # ###############################################################
        
        ##BBC RADIO

        yield Request("http://www.bbc.co.uk/radio1/playlist/",meta={'source':'BBC Radio',},callback=self.each_detail)
        
        ##Captal FM Playlist

        yield Request("http://www.capitalfm.com/on-air/playlist/",meta={'source':'Captal FM Playlist'},callback=self.each_detail)
        
        ##Kiss FM and kiss fm fresh

        yield Request("http://www.kissfmuk.com/playlists/",meta={'source':'Kiss FM'},callback=self.each_detail)

        ##J Play tracks
        
        yield Request("http://www.jplay.com.au/JSite/",meta={'source':"JPlay"},callback=self.each_detail)
        
        ##AirCheck National Radio Airplay Chart

        if self.todays_date==3: #thursday
            yield Request("https://www.radioinfo.com.au/knowledge/chart",meta={'source':'AirCheck'},callback=self.each_detail)
        
        ##Triple J

        yield Request("http://triplejgizmo.abc.net.au:8080/jjj-hitlist/current/app/webroot/latest/play.txt",meta={'source':'Triple J'},callback=self.each_detail)
        
        ##The Edge

        yield Request("http://www.theedge.co.nz/Music/Fat40.aspx",meta={'source':'The Edge'},callback=self.each_detail)
        
        ##The Much

        yield Request("http://www.much.com/shows/countdown/",meta={'source':"The Much"},callback=self.each_detail)
        
        ##The Edge top 30
        if self.todays_date==3: #thursday
            yield Request("http://www.edge.ca/edgetop30/",meta={'source':'The Edge 30'},callback=self.each_detail)
        
        ##Digilistan Sweden Radio

        yield Request("http://sverigesradio.se/sida/topplista.aspx?programid=2697",meta={'source':'Digilistan'},callback=self.each_detail)
        
        ##NRK sweden

        yield Request("http://p3.no/spillelister/?visning=topplister",meta={'source':'NRK Sweden'},callback=self.each_detail)
        
        ##NRK Norway

        yield Request("http://www.nrk.no/mp3/mp3topp30/",meta={'source':'NRK Norway'},callback=self.each_detail)
        
        ##NRJ

        yield Request("http://www.nrj.fr/playlists/vos-hits-nrj",meta={'source':'NRJ'},callback=self.each_detail)
        
        ##german radio charts

        yield Request("http://www.radiocharts.com/html/charts_de_main.htm",meta={'source':'German Radio Charts'},callback=self.each_detail)
        
        #Radio Callouts

        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[1].strip()=="Radio Callouts":
                    links.append(row)
                else:
                    count=count+1

        today=datetime.date.today()
        self.prevthursday(today)

        if self.todays_date==5: #saturday
            for l in links:
                yield Request(l[4].strip()+str(lastthursdate)+"&newPage=Show+Report",meta={'source':'Radio Callouts','chart_name':l[3].strip()},callback=self.each_detail)

        # Selenium
        now = datetime.date.today()
        date=now.strftime("%m/%d/%Y")
        
        #self.driver=webdriver.Chrome("chromedriver.exe")
        self.driver=webdriver.Firefox()
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="Spotify Flash Website":
                    links.append(row)
                else:
                    count=count+1

        
        #mediabase

        self.driver.get("http://www.mediabase.com/")
        inputElement = self.driver.find_element_by_name("userName")
        inputElement.send_keys("IDJMG258")
        inputElement = self.driver.find_element_by_name("password")
        inputElement.send_keys("Dmassey")
        inputElement.submit()
        time.sleep(2)
        mbhpage2="http://www.mediabase.com/weblogon/ValidateLogonMIS.asp?UserName=IDJMG258&Password=dmassey"
        self.driver.get(mbhpage2)

        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="Mediabase.com" and (row[1].strip()=="Published Radio" or row[1].strip()=="Building Radio" or row[1].strip()=="Building Radio Station Playlists"):
                    links.append(row)
                else:
                    count=count+1

        select_count=0
        for l in links:
            self.driver.get(l[4])
            time.sleep(2)
            if select_count==0:
                try:
                    Select(self.driver.find_element_by_name("SHOWTOPn")).select_by_visible_text("Show Top 1000")
                    time.sleep(2)
                    select_count=select_count+1
                except:
                    pass

            sel=Selector(text=self.driver.page_source)

            if l[1]=="Published Radio" and self.todays_date==6:
            #published radio
                chart_name=l[3]
                chart_type="Published Radio"

                peak_rank=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[1]/span/text()').extract()
                rank=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[3]/span/text()').extract()
                artist=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[8]/span/a/text()').extract()
                song=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[9]/span/a[2]/text()').extract()
                label=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[10]/span/text()').extract()
                spins=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[12]/span/text()').extract()
                spins_move=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[14]/span/text()').extract()
                audience=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[20]/span/text()').extract()
                audience_move=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=1 and not(position()>=10000)]/td[22]/span/text()').extract()

                index=0
                for p in peak_rank:
                    try:
                        sql = "INSERT INTO %s (Artist,Song,Label,Spins,Spin_move,Audience,Audience_move,Chart_name,Chart_type,Rank,Peak,Date) \
                        values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                      escape_string("".join(artist[index]).encode('utf-8')),
                      escape_string("".join(song[index]).encode('utf-8')),
                      escape_string("".join(label[index]).encode('utf-8')),
                      escape_string("".join(spins[index]).encode('utf-8')),
                      escape_string("".join(spins_move[index]).encode('utf-8')),
                      escape_string("".join(audience[index]).encode('utf-8')),
                      escape_string("".join(audience_move[index]).encode('utf-8')),
                      escape_string("".join(chart_name).encode('utf-8')),
                      escape_string("".join(chart_type).encode('utf-8')),
                      escape_string("".join(rank[index]).encode('utf-8')),
                      escape_string("".join(p).encode('utf-8')),
                      now,
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"
                    except Exception,e:
                        raise e
                        print e.message
                        pass
                
                    index=index+1

            if l[1]=="Building Radio":
            #building radio
                chart_name=l[3]
                chart_type="Building Radio"

                rank=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[2]/span/text()').extract()
                artist=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[7]/span/text()').extract()
                song=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[9]/a/text()').extract()
                label=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[10]/span/text()').extract()
                spins=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[12]/span/text()').extract()
                spins_move=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[14]/span/text()').extract()
                audience=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[22]/span/text()').extract()
                audience_move=sel.xpath('//*[@id="Table4"]/thead/tr[position()>=3 and not(position()>=10000)]/td[24]/span/text()').extract()
                
                index=0
                for r in rank:
                    try:
                        sql = "INSERT INTO %s (Artist,Song,Label,Spins,Spin_move,Audience,Audience_move,Chart_name,Chart_type,Rank,Date) \
                        values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                      escape_string("".join(artist[index]).encode('utf-8')),
                      escape_string("".join(song[index]).encode('utf-8')),
                      escape_string("".join(label[index]).encode('utf-8')),
                      escape_string("".join(spins[index]).encode('utf-8')),
                      escape_string("".join(spins_move[index]).encode('utf-8')),
                      escape_string("".join(audience[index]).encode('utf-8')),
                      escape_string("".join(audience_move[index]).encode('utf-8')),
                      escape_string("".join(chart_name).encode('utf-8')),
                      escape_string("".join(chart_type).encode('utf-8')),
                      escape_string("".join(r).encode('utf-8')),
                      now,
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"
                    except Exception,e:
                        raise e
                        print e.message
                        pass
                
                    index=index+1

            if l[1]=="Building Radio Station Playlists":
                chart_name=l[3]
                chart_type="Building Radio Station Playlists"
  
            #building radio station playlist

                title=sel.xpath('//*[@class="Title"]/text()').extract()
                #title=sel.xpath('//*[@class="Title"][1]/text()').extract()
                #title=sel.xpath('//*[@class="Title"][position()>=1 and not(position()>=2)]/text()').extract()
                subtitle=sel.xpath('//*[@class="subtitlelink"][position()>=1 and not (position()>=2)]/a/text()').extract()
                chart_name="".join(title[0]).strip() +" " +"".join(subtitle[0]).strip() +" " +"".join(subtitle[1]).strip()
                rank=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[3]/text()').extract()
                artist=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[4]/a/text()').extract()
                song=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[6]/a/text()').extract()
                label=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[7]/a/text()').extract()
                spins=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[8]/a/text()').extract()
                spins_move=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[10]/a/text()').extract()
                
                index=0
                for r in rank:
                    try:
                        sql = "INSERT INTO %s (Artist,Song,Label,Spins,Spin_move,Chart_name,Chart_type,Rank,Date) \
                        values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                      escape_string("".join(artist[index]).encode('utf-8')),
                      escape_string("".join(song[index]).encode('utf-8')),
                      escape_string("".join(label[index]).encode('utf-8')),
                      escape_string("".join(spins[index]).encode('utf-8')),
                      escape_string("".join(spins_move[index]).encode('utf-8')),
                      escape_string("".join(chart_name).encode('utf-8')),
                      escape_string("".join(chart_type).encode('utf-8')),
                      escape_string("".join(r).encode('utf-8')),
                      now,
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"
                    except Exception,e:
                        raise e
                        print e.message
                        pass
                
                    index=index+1

        
        #radio add boards mediaboard
        
        self.driver.get("http://addboard.mediabase.com/SignIn.asp")
        
        inputElement = self.driver.find_element_by_name("Username")
        inputElement.send_keys("IDJMG258")
        inputElement = self.driver.find_element_by_name("PASSWORD")
        inputElement.send_keys("Dmassey")
        inputElement.submit()
        time.sleep(2)
        
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="Mediabase.com" and row[1].strip()=="Radio Add Boards":
                    links.append(row)
                else:
                    count=count+1

        for l in links:
            if l[3].strip()=="Hot AC" or l[3].strip()=="AAA":
                if self.todays_date==1: # tuesday, even tho finishes monday 7pm
                    chart_type="Radio Add Boards"
                    self.driver.get(l[4])
                    time.sleep(2)
                    sel=Selector(text=self.driver.page_source)

                    no_adds=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[1]/text()').extract()
                    artist=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[2]/a/text()').extract()
                    song=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[3]/a[2]/text()').extract()
                    label=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[4]/text()').extract()
                    top_historic_adds=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[5]/a/text()').extract()
                    chart_name=sel.xpath('//*[@class="title"]/text()').extract()


                    index=0
                    for a in no_adds:
                        no_of_adds=a
                        rank=index+1
                        temp_chart_name="".join(chart_name).strip()
                        temp_artist="".join(artist[index]).strip()
                        temp_song="".join(song[index]).strip()
                        temp_label="".join(label[index]).strip()
                        temp_historic_adds="".join(top_historic_adds[index]).strip()
                        
                        try:
                            sql = "INSERT INTO %s (Artist,Song,Label,no_of_Adds,top_historic_Adds, Chart_name,Chart_type,Rank,Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string("".join(temp_artist).encode('utf-8')),
                              escape_string("".join(temp_song).encode('utf-8')),
                              escape_string("".join(temp_label).encode('utf-8')),
                              escape_string("".join(no_of_adds).encode('utf-8')),
                              escape_string("".join(temp_historic_adds).encode('utf-8')),
                              escape_string("".join(temp_chart_name).encode('utf-8')),
                              escape_string("".join(chart_type).encode('utf-8')),
                              escape_string("".join(str(rank)).encode('utf-8')),
                              now,
                              )

                            global x
                            if x.execute(sql):
                                print "item Inserted"
                            else:
                                print "Something wrong"
                        except:
                            pass
                        
                        index=index+1

            else:
                if self.todays_date==2: # wednesday, even tho finishes tuesday at 7pm
                        chart_type="Radio Add Boards"
                        self.driver.get(l[4])
                        time.sleep(2)
                        sel=Selector(text=self.driver.page_source)

                        no_adds=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[1]/text()').extract()
                        artist=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[2]/a/text()').extract()
                        song=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[3]/a[2]/text()').extract()
                        label=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[4]/text()').extract()
                        top_historic_adds=sel.xpath('//*[@class="report"]/table/tbody/tr[position()>=3 and not(position()>=10000)]/td[5]/a/text()').extract()
                        chart_name=sel.xpath('//*[@class="title"]/text()').extract()


                        index=0
                        for a in no_adds:
                            no_of_adds=a
                            rank=index+1
                            temp_chart_name="".join(chart_name).strip()
                            temp_artist="".join(artist[index]).strip()
                            temp_song="".join(song[index]).strip()
                            temp_label="".join(label[index]).strip()
                            temp_historic_adds="".join(top_historic_adds[index]).strip()
                            
                            try:
                                sql = "INSERT INTO %s (Artist,Song,Label,no_of_Adds,top_historic_Adds, Chart_name,Chart_type,Rank,Date) \
                                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                                  escape_string("".join(temp_artist).encode('utf-8')),
                                  escape_string("".join(temp_song).encode('utf-8')),
                                  escape_string("".join(temp_label).encode('utf-8')),
                                  escape_string("".join(no_of_adds).encode('utf-8')),
                                  escape_string("".join(temp_historic_adds).encode('utf-8')),
                                  escape_string("".join(temp_chart_name).encode('utf-8')),
                                  escape_string("".join(chart_type).encode('utf-8')),
                                  escape_string("".join(str(rank)).encode('utf-8')),
                                  now,
                                  )

                                global x
                                if x.execute(sql):
                                    print "item Inserted"
                                else:
                                    print "Something wrong"
                            except:
                                pass
                            
                            index=index+1

        self.driver.quit()

            #self.driver.quit()

   
      ##spotify playlists (API)
        def show_tracks(results):
            for i, item in enumerate(tracks['items']):
                track = item['track']
                listy = [track['artists'][0]['name'],track['name'],track['album']['name'],i+1]
                spotifylist.append(listy)
        
        SPOTIPY_CLIENT_ID='71d62390b02c463dad997e6ce527d102'
        SPOTIPY_CLIENT_SECRET='14014e506f224ed0a61db58bb71d73d7'
        SPOTIPY_REDIRECT_URI='http://google.com'
        scope = 'user-library-read'
        
        username = 'spotify'
        token = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        #if it expires, spotify will direct u to a url and ask you to enter the url you were directed to - follow those instructions and carry on to next parts of this code!
        #if THAT doesnt work, go to https://developer.spotify.com/web-api/console/get-playlists/ & manually generate token (user library read) & put in below
        #token = "BQDBi85nJJ1WCW5fv_TcEgwmY-kB1cNB9nrHC3ICqPHnGwsyLylCYKsZ4S8g_St5zY8V_YdwsacbanwPLw4mai2A2R5NibZzDDUSLzyX5CTooQRcGYfQ886KUjfkBpEQQLo7v1iVsIt5yyGVQDsC-rnQU3OwSMFTqHje6ts"
        sp = spotipy.Spotify(auth=token)
        
        username2 = 'lmljoe'
        token2 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        #token2 = "BQDjeU8dZTKjsKK-AOr3geNCqSByoMm-ABFanKN-NmuRBNcymGF8EfANCV_B1AozABljJMB9lBMZOiVx2podMwiQxn6WzLFej0OBGlkH5dD291nZFYhjFvuVni0OWuw1fKeu9G6PtEyz9ER4w7ibOhKbvSLQTgnkLLCHT-g"
        sp2 = spotipy.Spotify(auth=token2)
        
        username3 = 'myplay.com'
        token3 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        #token3 = "BQAirwgjE1A-DojGah0RzpCuXUjarC5WMSBAhsX9jD8Zcibuo5pBzVdCO_GOSqNYpmU-_fqXPS4ORswrKG7x1UzOLNqXhk60kdq_2ovVIvikKFDTUxNxHaf-uHAI3OY6-esZ8nJt2d8MX55kiaESRMx2aDbSLUwtrM_2DiQ"
        sp3 = spotipy.Spotify(auth=token3)
        
        username4 = 'digster.fm'
        token4 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        #token4 = "...."
        sp4 = spotipy.Spotify(auth=token4)

        username5 = 'pbowlesy'
        token5 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        #token4 = "...."
        sp5 = spotipy.Spotify(auth=token5)
        
        ####Spotify-Curated Playlists####
        #Today's Top Hits Spotify Playlist
        id = '5FJXhjdILmRA2z5bvz4nzf'
        TopHitsPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = TopHitsPlaylist['tracks']
        TopHitsPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        TopHitsPlaylist = spotifylist
        for spot in TopHitsPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist,Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Today's Top Hits Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(TopHitsPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except Exception,e:
                print e.message
                raise e
                pass

        #Teen Party Playlist
        id = '3MlpudZs4HT3i0yGPVfmHC'
        TeenPartyPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = TeenPartyPlaylist['tracks']
        TeenPartyPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        TeenPartyPlaylist = spotifylist
        for spot in TeenPartyPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist,Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Teen Party Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(TeenPartyPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except Exception,e:
                print e.message
                raise e
                pass
                       
        #Fresh Finds Spotify Playlist
        id = '3rgsDhGHZxZ9sB9DQWQfuf'
        FreshFindsPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = FreshFindsPlaylist['tracks']
        FreshFindsPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        FreshFindsPlaylist = spotifylist
        for spot in FreshFindsPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist,Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Fresh Finds Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(FreshFindsPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
        #Viral Hits Spotify Playlist
        id = '2qTeRwnwFquJUKrAFWnolb'
        ViralHitsPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = ViralHitsPlaylist['tracks']
        ViralHitsPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        ViralHitsPlaylist = spotifylist
        for spot in ViralHitsPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist,Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Viral Hits Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(ViralHitsPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
        #Mood Booster Spotify Playlist
        id = '6uTuhSs7qiEPfCI3QDHXsL'
        MoodBoosterPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = MoodBoosterPlaylist['tracks']
        MoodBoosterPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        MoodBoosterPlaylist = spotifylist
        for spot in MoodBoosterPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Mood Booster Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(MoodBoosterPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
        if self.todays_date==4: #Friday
            #New Music Friday Spotify Playlist
            id = '1yHZ5C3penaxRdWR7LRIOb'
            NewMusicFriPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
            tracks = NewMusicFriPlaylist['tracks']
            NewMusicFriPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
            spotifylist=list()
            show_tracks(tracks)
            NewMusicFriPlaylist = spotifylist
            for spot in NewMusicFriPlaylist:
                try:
                    now = datetime.date.today()
                    sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                                  escape_string(spot[0].encode('utf-8').strip()),
                                  escape_string(spot[1].encode('utf-8').strip()),
                                  escape_string(spot[2].encode('utf-8').strip()),
                                  escape_string("".join("New Music Friday Playlist").encode('utf-8').strip()),
                                  escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                                  escape_string(str(spot[3]).strip()),
                                  escape_string(str(NewMusicFriPlaylistFollowers).encode('utf-8').strip()),
                                  now,
                                  )
    
                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"
                except:
                    pass
            
        #Digging Now Playlist
        id = '2YoVrFsJPvunjHQYfM12cP'
        DiggingNowSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = DiggingNowSpotPlaylist['tracks']
        DiggingNowSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        DiggingNowSpotPlaylist = spotifylist
        for spot in DiggingNowSpotPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Digging Now Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(DiggingNowSpotPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except Exception,e:
                raise e
                pass
            
        #The Indie Mix Spotify Playlist
        id = '75dwLdmL07hDEDWqX17QeE'
        IndieMixSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = IndieMixSpotPlaylist['tracks']
        IndieMixSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        IndieMixSpotPlaylist = spotifylist
        for spot in IndieMixSpotPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Indie Mix Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(IndieMixSpotPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
        #Indie Pop! Spotify Playlist
        id = '2ikvjqFDwalfKdCHkxn79O'
        IndiePopSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        tracks = IndiePopSpotPlaylist['tracks']
        IndiePopSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        IndiePopSpotPlaylist = spotifylist
        for spot in IndiePopSpotPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Indie Pop! Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(IndiePopSpotPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
        ####myplay.com-Curated Playlists####
        
        #Top of the Charts Spotify Playlist
        id = '4ANVDtJVtVMVc2Nk79VU1M'
        TopOfChartsSpotPlaylist = sp3.user_playlist(username3, playlist_id=id, fields="tracks,next")
        tracks = TopOfChartsSpotPlaylist['tracks']
        TopOfChartsSpotPlaylistFollowers = sp.user_playlist(username3, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        TopOfChartsSpotPlaylist = spotifylist
        for spot in TopOfChartsSpotPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Filtr Top Of The Charts Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(TopOfChartsSpotPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
        ####digster.fm-Curated Playlists####
        
        #Hits Spotify Playlist
        id = '4noDy1IQejcxDbTLvzuWhS'
        HitsDigsterSpotPlaylist = sp4.user_playlist(username4, playlist_id=id, fields="tracks,next")
        tracks = HitsDigsterSpotPlaylist['tracks']
        HitsDigsterSpotPlaylistFollowers = sp.user_playlist(username4, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        HitsDigsterSpotPlaylist = spotifylist
        for spot in HitsDigsterSpotPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Digster Poptopia Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(HitsDigsterSpotPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass
        
       ####Peter Blowlesy-Curated Playlists####
        
        #Apple Beats Playlist
        id = '0i9MrcCGZa8Sd3oEdjjca4'
        BeatsSpotPlaylist = sp5.user_playlist(username5, playlist_id=id, fields="tracks,next")
        tracks = BeatsSpotPlaylist['tracks']
        BeatsSpotPlaylistFollowers = sp.user_playlist(username5, playlist_id=id, fields="followers")['followers']['total']
        spotifylist=list()
        show_tracks(tracks)
        BeatsSpotPlaylist = spotifylist
        for spot in BeatsSpotPlaylist:
            try:
                now = datetime.date.today()
                sql = "INSERT INTO %s (Artist,Song,Album,Chart_name,Chart_type,Rank,Playlist, Date) \
                                values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                              escape_string(spot[0].encode('utf-8').strip()),
                              escape_string(spot[1].encode('utf-8').strip()),
                              escape_string(spot[2].encode('utf-8').strip()),
                              escape_string("".join("Apple Beats Playlist").encode('utf-8').strip()),
                              escape_string("".join("Spotify Playlists").encode('utf-8').strip()),
                              escape_string(str(spot[3]).strip()),
                              escape_string(str(BeatsSpotPlaylistFollowers).encode('utf-8').strip()),
                              now,
                              )

                global x
                if x.execute(sql):
                    print "item Inserted"
                else:
                    print "Something wrong"
            except:
                pass

    def prevthursday(self,input):
        from datetime import date, timedelta, time
        today = input
        offset = (today.weekday() - 4) % 7
        thursday = today - timedelta(days=offset)
        # import datetime
        # todaysdate = datetime.date.today()
        # #if today = sun or sat or fri, or thurs, select the thursday from 2 wks ago - not most recent thursday
        # if todaysdate.weekday() == 6 or todaysdate.weekday() == 5 or todaysdate.weekday() == 4 or todaysdate.weekday() == 3:
        #     thursday=today - (timedelta(days=offset+7)) 
        global lastthursdate
        lastthursdate = thursday


   

    def each_detail(self,response):
        #open_in_browser(response)
        
        sel=Selector(response)
        
        source=response.meta['source']
        # spotify charts website
        
    
        if source=="Spotify Charts Website":
            sel=Selector(response)
            rank=sel.xpath('//*[@class="chart-table-position"]/text()').extract()
            song=sel.xpath('//*[@class="chart-table-track"]/strong/text()').extract()
            artist=sel.xpath('//*[@class="chart-table-track"]/span/text()').extract()
            spotify=sel.xpath('//*[@class="chart-table-streams"]/text()').extract()
            chart_name=sel.xpath('//*[@class="chart-page"]/li[1]/a/text()').extract()
            chart_name_2=sel.xpath('//*[@class="chart-filters-list"]/div[1]/div/text()').extract()
            chart_type="Spotify"
            
            
            index=0
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            for r in rank:
                try:
                    temp_stream="".join(spotify[index+1]).strip().replace(',','')
                    temp_stream=int(temp_stream)
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Spotify,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist[index].split('by')[1]).encode('utf-8').strip()),
                  escape_string("".join(song[index]).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_name_2).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string("".join(r).strip()),
                  temp_stream,
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"
                except Exception,e:
                    print e
                    raise e
                    pass
                
                index=index+1


    def each_detail(self,response):
        #open_in_browser(response)
        
        sel=Selector(response)
        
        source=response.meta['source']
        # spotify charts website
        
    
        if source=="Spotify Charts Website":
            sel=Selector(response)
            rank=sel.xpath('//*[@class="chart-table-position"]/text()').extract()
            song=sel.xpath('//*[@class="chart-table-track"]/strong/text()').extract()
            artist=sel.xpath('//*[@class="chart-table-track"]/span/text()').extract()
            spotify=sel.xpath('//*[@class="chart-table-streams"]/text()').extract()
            chart_name=sel.xpath('//*[@class="chart-page"]/li[1]/a/text()').extract()
            chart_name_2=sel.xpath('//*[@class="chart-filters-list"]/div[1]/div/text()').extract()
            chart_type="Spotify"
            
            
            index=0
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            for r in rank:
                try:
                    temp_stream="".join(spotify[index+1]).strip().replace(',','')
                    temp_stream=int(temp_stream)
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Spotify,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist[index].split('by')[1]).encode('utf-8').strip()),
                  escape_string("".join(song[index]).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_name_2).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string("".join(r).strip()),
                  temp_stream,
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"
                except Exception,e:
                    print e
                    raise e
                    pass
                
                index=index+1

    #     # shazam
        if source=="Viral":
            sel=Selector(response)
            rank=sel.xpath('//*[@class="chart-table-position"]/text()').extract()
            song=sel.xpath('//*[@class="chart-table-track"]/strong/text()').extract()
            artist=sel.xpath('//*[@class="chart-table-track"]/span/text()').extract()
            chart_name=sel.xpath('//*[@class="chart-page"]/li[2]/a/text()').extract()
            chart_name_2=sel.xpath('//*[@class="chart-filters-list"]/div[1]/div/text()').extract()
            chart_type="Spotify"

            
            index=0
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
                
            
            for r in rank:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist[index].split('by')[1]).encode('utf-8').strip()),
                  escape_string("".join(song[index]).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_name_2).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string("".join(r).strip()),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"
                except Exception,e:
                    raise e
                
                index=index+1

    #     # shazam
        if source=="Shazam.com":
            sel=Selector(response)
            rank=sel.xpath('//*[@itemprop="track"]/@data-chart-position').extract()
            song=sel.xpath('//*[@class="ti__title"]/a/text()').extract()
            artist=sel.xpath('//*[@class="ti__artist"]/meta/@content').extract()
            no_of_shazams=sel.xpath('//*[@class="ti__tagcount"]/span/text()').extract()
            temp_1=sel.xpath('//*[@class="chrt-nav__select__details"]/text()').extract()
            #temp_2=sel.xpath('//*[@class="chrt-nav__select__details"][2]/text()').extract()
            chart_name="".join(temp_1[0]).strip()
            chart_name_2="".join(temp_1[1]).strip()
            chart_type=response.meta['chart_type']
            index=0
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            for r in rank:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Shazams,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist[index]).encode('utf-8').strip()),
                  escape_string("".join(song[index]).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_name_2).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string("".join(r).strip()),
                  escape_string("".join(no_of_shazams[index]).encode('utf-8').strip()),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"
                except:
                    pass
                
                index=index+1

                

        # Itunes

        if source=="iTunes RSS":
            chart_name=response.meta['chart_name']
            chart_name_2=response.meta['chart_name_2']
            chart_type=response.meta['chart_type']
            chart=response.meta['chart']

            f=open("temp.xml",'w+b')
            f.write(response.body)
            f.close()

            DOMTree = xml.dom.minidom.parse("temp.xml")
            collection = DOMTree.documentElement
            entries = collection.getElementsByTagName("entry")

            rank=1

            song=""
            artist=""
            album=""
            price=""
            genre=""
            release_date=""
            label=""
            final_label=""

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            for e in entries:
                try:
                    song=e.getElementsByTagName('im:name')[0].childNodes[0].data
                except:
                    pass
                try:
                    artist=e.getElementsByTagName('im:artist')[0].childNodes[0].data
                except:
                    pass
                try:
                    album=e.getElementsByTagName('im:collection')[0].getElementsByTagName('im:name')[0].childNodes[0].data
                except:
                    pass
                try:
                    price=e.getElementsByTagName('im:price')[0].childNodes[0].data
                except:
                    pass
                try:
                    genre=e.getElementsByTagName('category')[0].getAttribute('term')
                except:
                    pass
                try:
                    release_date=e.getElementsByTagName('im:releaseDate')[0].getAttribute('label')
                except:
                    pass
                try:
                    label=e.getElementsByTagName('content')[0].childNodes[0].data
                except:
                    pass
                try:
                    label="".join(label).encode('ascii','ignore')
                    label=label.split('<font')
                    final_label=label[len(label)-1].split('</font>')[0].split('>')[1].split(';')[1]
                except:
                    pass

                try:
                    # temp="".join(chart_name).split()[0]
                    # chart_name_2="".join(chart_name).split()[1].replace('(','').replace(')','').strip()

                    if chart=="Song":
                        sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Album,Price,Genre,ReleaseDate,Label,Date) \
                        values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                      escape_string(artist.encode('utf-8').strip()),
                      escape_string(song.encode('utf-8').strip()),
                      escape_string(chart_name.encode('utf-8').strip()),
                      escape_string(chart_name_2.encode('utf-8').strip()),
                      escape_string(chart_type.encode('utf-8').strip()),
                      escape_string(str(rank)),
                      escape_string(album.encode('utf-8').strip()),
                      escape_string(price.encode('utf-8').strip()),
                      escape_string(genre.encode('utf-8').strip()),
                      escape_string(release_date),
                      escape_string("".join(final_label).encode('utf-8').strip()),
                      now,
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"

                    elif chart=="Album":
                        sql = "INSERT INTO %s (Artist,Chart_name,Chart_name_2,Chart_type,Rank,Album,Price,Genre,ReleaseDate,Label,Date) \
                        values('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ("album_chart",
                      escape_string(artist.encode('utf-8').strip()),
                      escape_string(chart_name.encode('utf-8').strip()),
                      escape_string(chart_name_2.encode('utf-8').strip()),
                      escape_string(chart_type.encode('utf-8').strip()),
                      escape_string(str(rank)),
                      escape_string(song.encode('utf-8').strip()),
                      escape_string(price.encode('utf-8').strip()),
                      escape_string(genre.encode('utf-8').strip()),
                      escape_string(release_date),
                      escape_string("".join(final_label).encode('utf-8').strip()),
                      now,
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"

                except Exception,e:
                    raise e
                    print e.message
                    

                rank=rank+1
            

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
                    values('%s', '%s', '%s', '%s','%s','%s','%s')" % ("songs_chart",
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
                            print "item Inserted"
                        else:
                            print "Something wrong"

                    except Exception,e:
                        raise e
                        pass
                        

                    rank=rank+1
                    
        #Twitter

        if source=="Realtime.Billboard.com":
            chart_name=response.meta['chart_name']
            chart_type=response.meta['chart_type']
            chart=response.meta['chart']

            f=open("temp.json",'w+b')
            f.write(response.body)
            f.close()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            with open("temp.json") as json_file:
                json_data = json.load(json_file)
                total_results=json_data["results"]
                
                for t in total_results:
                    rank=t["position"]
                    chart_name="Emerging Artist"
                    song=t["name"]
                    artist=t["artist"]["name"]

                    try:
                        sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string(artist.encode('utf-8').strip()),
                  escape_string(song.encode('utf-8').strip()),
                  escape_string(chart_name.encode('utf-8').strip()),
                  escape_string(chart_type.encode('utf-8').strip()),
                  escape_string(str(rank)),
                  now,
                  )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"

                    except Exception,e:
                        raise e
                        pass
                        

                    

        #Hype Machine

        if source=="HypeM.com":
            chart_type=response.meta['chart_type']
            chart_name=response.meta['chart_name']
            chart=response.meta['chart']

            artist=sel.xpath('//*[@class="artist"]')
            song=sel.xpath('//*[@class="base-title"]')
            rank=sel.xpath('//*[@class="rank"]')
            no_of_blogs=sel.xpath('//*[@class="buy"]')

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            for index in range(0,len(artist)):
                item=MusicItem()
                temp_rank=rank[index].xpath('text()').extract()
                temp_song=song[index].xpath('text()').extract()
                temp_artist=artist[index].xpath('text()').extract()
                temp=no_of_blogs[index].xpath('a/text()').extract()
                try:
                    temp="".join(temp).split('by')[1].strip().split()[0].strip()
                except:
                    pass
                    temp=""

                temp_blog=temp
                
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_type,Rank,Blogs,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(temp_artist).encode('utf-8').strip()),
                  escape_string("".join(temp_song).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string("".join(temp_rank).encode('utf-8').strip()),
                  escape_string("".join(temp_blog).encode('utf-8').strip()),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except:
                    pass
            

        #bbc radio
        if source=="BBC Radio":
            song_a=sel.xpath('//*[@id="a"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-title"][1]/text()').extract()
            artist_a=sel.xpath('//*[@id="a"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-artist"][1]/a/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_a:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_a[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "BBC Radio A List",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                rank=rank+1
                index=index+1

            song_b=sel.xpath('//*[@id="b"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-title"][1]/text()').extract()
            artist_b=sel.xpath('//*[@id="b"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-artist"][1]/a/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_b:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_b[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "BBC Radio B List",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1


            song_c=sel.xpath('//*[@id="c"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-title"][1]/text()').extract()
            artist_c=sel.xpath('//*[@id="c"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-artist"][1]/a/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_c:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_c[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "BBC Radio C List",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

            song_inmwt=sel.xpath('//*[@id="inmwt"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-title"][1]/text()').extract()
            artist_inmwt=sel.xpath('//*[@id="inmwt"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-artist"][1]/a/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_inmwt:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_inmwt[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "BBC In New Music We Trust List",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

            song_intd=sel.xpath('//*[@id="introducing"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-title"][1]/text()').extract()
            artist_intd=sel.xpath('//*[@id="introducing"]/div[position()>=1 and not(position()>=1000)]//div[@class="pll-playlist-item-artist"][1]/a/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_intd:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_intd[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "BBC Introducing",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

        # capital FM Playlist

        if source=="Captal FM Playlist":
            songs=sel.xpath('//*[@class="song_wrapper"]/h3')
            #songs_2=sel.xpath('//*[@class="song_wrapper"]/h3/span[@class="track"]')
            #songs=songs_1+songs_2
            artists=sel.xpath('//*[@class="song_wrapper"]/h3/span[@itemprop="byArtist"]')
            

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in songs:
                temp_song=s.xpath('span[@class="track"]/text()').extract()
                if len("".join(temp_song))<=0:
                    temp_song=s.xpath('a[@class="track"]/text()').extract()

                temp_artist=artists[index].xpath('.//text()').extract()
                try:
                    temp_artist="".join(temp_artist).split()
                except:
                    pass

                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string(" ".join(temp_artist).encode('utf-8').strip()),
                  escape_string("".join(temp_song).encode('utf-8').strip()),
                  "Capital FM Playlist",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

        #KISS FM

        if source=="Kiss FM":
            song_kiss=sel.xpath('//*[@class="playlist-widget__kiss"]/ul/li[position()>=1 and not(position()>=1000)]/div[2]/p[2]/text()').extract()
            artist_kiss=sel.xpath('//*[@class="playlist-widget__kiss"]/ul/li[position()>=1 and not(position()>=1000)]/div[2]/p[1]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            index=0
            rank=1
            for s in song_kiss:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_kiss[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "Kiss FM",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

            song_kiss_fresh=sel.xpath('//*[@class="playlist-widget__kissfresh"]/ul/li[position()>=1 and not(position()>=1000)]/div[2]/p[2]/text()').extract()
            artist_kiss_fresh=sel.xpath('//*[@class="playlist-widget__kissfresh"]/ul/li[position()>=1 and not(position()>=1000)]/div[2]/p[1]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_kiss_fresh:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_kiss_fresh[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "Kiss FM Fresh",
                  "UK",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

        #JPlay
        if source=="JPlay":
            song_added=sel.xpath('//*[@id="dgMostRecentAddedSongs"]/tr[position()>=2 and not(position()>=1000)]/td[2]/a/text()').extract()
            artist_added=sel.xpath('//*[@id="dgMostRecentAddedSongs"]/tr[position()>=2 and not(position()>=1000)]/td[1]/a/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_added:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_added[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "J Play Most Recently Added Tracks",
                  "Australia",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

            song_played=sel.xpath('//*[@id="dgMostPlayedSongsInWeek"]/tr[position()>=2 and not(position()>=1000)]/td[2]/a[2]/text()').extract()
            artist_played=sel.xpath('//*[@id="dgMostPlayedSongsInWeek"]/tr[position()>=2 and not(position()>=1000)]/td[2]/a[1]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            rank=1
            for s in song_played:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist_played[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "J Play Most Played Tracks",
                  "Australia",
                  "International Radio",
                  escape_string(str(rank)),
                  now,
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                rank=rank+1
                index=index+1

        if source=="AirCheck":
            songs=sel.xpath('//td[@class="title"]/text()').extract()
            artists=sel.xpath('//td[@class="artist"]/text()').extract()
            rank=sel.xpath('//td[@class="twRank"]/text()').extract()
            label=sel.xpath('//td[@class="distribution"]/text()').extract()
            spins=sel.xpath('//td[@class="twSpins"]/text()').extract()
            spins_move=sel.xpath('//td[@class="differenceSpins"]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date,Spins,Spin_move,Label) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "AirCheck National Radio Airplay Chart",
                  "Australia",
                  "International Radio",
                  escape_string("".join(rank[index]).strip()),
                  now,
                  escape_string("".join(spins[index]).strip()),
                  escape_string("".join(spins_move[index]).strip()),
                  escape_string("".join(label[index]).strip())
                  
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    pass

                index=index+1

        if source=="Triple J":
            
            f=open("temp.json",'w+b')
            f.write(response.body)
            f.close()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            with open("temp.json") as json_file:
                json_data = json.load(json_file)
                
                rank=1

                index=0
                for t in json_data:
                    song=t["HitlistEntry"]["track"]
                    artist=t["HitlistEntry"]["artist"]
                    label=t["HitlistEntry"]["label_name"]
                    try:
                        sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date,Label) \
                        values('%s', '%s', '%s','%s', '%s','%s','%s','%s')" % ("songs_chart",
                      escape_string("".join(artist).strip().encode('utf-8')),
                      escape_string("".join(song).encode('utf-8').strip()),
                      "Triple J: The Hit List",
                      "Australia",
                      "International Radio",
                      escape_string(str(rank)),
                      now,
                      escape_string("".join(label).strip())
                      
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"

                    except Exception,e:
                        raise e

                    rank=rank+1
        

        if source=="The Edge":
            
            songs=sel.xpath('//tr[contains(@class,"Normal UDT_Table_")]/td[3]/text()').extract()
            artists=sel.xpath('//tr[contains(@class,"Normal UDT_Table_")]/td[2]/text()').extract()
            rank=sel.xpath('//tr[contains(@class,"Normal UDT_Table_")]/td[1]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "The Edge: Fat 40",
                  "New Zealand",
                  "International Radio",
                  escape_string("".join(rank[index]).strip()),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1
        

        if source=="The Much":
            
            songs=sel.xpath('//*[@class="song-info"]/a[1]/text()').extract()
            artists=sel.xpath('//*[@class="song-info"]/a[2]/text()').extract()
            rank=sel.xpath('//*[@class="col-xs-12 col-sm-6 col-md-4 countdown-video-item video-data"]/div[1]/span[1]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).strip().encode('utf-8')),
                  escape_string(s.encode('utf-8').strip()),
                  "The Much Video Countdown",
                  "Canada",
                  "International Radio",
                  escape_string("".join(rank[index]).strip()),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1

        if source=="The Edge 30":
            
            artist_song=sel.xpath('//*[@class="wpb_content_element span12 wpb_text_column"]/div/ol/li[position()>=1 and not(position()>=1000)]/text()').extract()
            
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            rank=1
            index=0
            for s in artist_song:
                
                temp_artist=s.encode('utf-8').split('–')[0]
                temp_song=s.encode('utf-8').split('–')[1]
                
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string(temp_artist.strip()),
                  escape_string(temp_song.strip()),
                  "101.2 The Edge Top 30",
                  "Canada",
                  "International Radio",
                  escape_string(str(rank)),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1
                rank=rank+1
        
        if source=="Digilistan":
            
            artist_song=sel.xpath('//*[@class="track-title"]/text()').extract()
            rank=sel.xpath('//*[@class="toplist-position"]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            index=0
            for s in artist_song:
                try:
                    temp=s.encode('utf-8').split('-')
                    temp_artist=temp[0]
                    temp_song=temp[1]

                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string(temp_artist.strip()),
                  escape_string(temp_song.strip()),
                  "DigiListan Swedish Radio",
                  "Sweden",
                  "International Radio",
                  escape_string("".join(rank[index]).strip()),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1


        if source=="NRK Sweden":
            
            songs=sel.xpath('//*[@class="tittel"]/text()').extract()
            artists=sel.xpath('//*[@class="songs"]/tr[position()>=2 and not(position()>=1000)]/td[2]/span[@class="artist"]/a/text()').extract()
            ranks=sel.xpath('//*[@class="songs"]/tr[position()>=2 and not(position()>=1000)]/td[1]/span/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).encode('utf-8').strip()),
                  escape_string("".join(s).encode('utf-8').strip()),
                  "NRK P3 30 Most Played",
                  "Sweden",
                  "International Radio",
                  escape_string("".join(ranks[index].replace('#','')).strip()),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1

        if source=="NRK Norway":
            
            songs=sel.xpath('//*[@class="entry"]/div[7]/table/tbody/tr[position()>=2 and not(position()>=1000)]/td[2]/text()').extract()
            artists=sel.xpath('//*[@class="entry"]/div[7]/table/tbody/tr[position()>=2 and not(position()>=1000)]/td[3]/text()').extract()
            ranks=sel.xpath('//*[@class="entry"]/div[7]/table/tbody/tr[position()>=2 and not(position()>=1000)]/td[1]/text()').extract()

            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).encode('utf-8').strip()),
                  escape_string("".join(s).encode('utf-8').strip()),
                  "NRK mP3 Top 30",
                  "Norway",
                  "International Radio",
                  escape_string("".join(ranks[index]).strip()),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1

        if source=="NRJ":
            
            songs=sel.xpath('//*[@class="ranking-track"]/text()').extract()
            artists=sel.xpath('//*[@class="ranking-artist"]/@title').extract()
            
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            rank=1
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).encode('utf-8').strip()),
                  escape_string("".join(s).encode('utf-8').strip()),
                  "Vos Hits NRJ",
                  "France",
                  "International Radio",
                  escape_string(str(rank).strip()),
                  now
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1
                rank=rank+1

        if source=="German Radio Charts":
            
            songs=sel.xpath('//*[@title="Titel"]/text()').extract()
            artists=sel.xpath('//*[@title="Interpret"]/text()').extract()
            ranks=sel.xpath('//*[@id="mainContentContainer"]/table/tbody/tr[position()>=1 and not(position()>=1000)]/td[2]/strong/text()').extract()
            label_1=sel.xpath('//*[@title="Label"]/text()').extract()
            label_2=sel.xpath('//*[@title="Vertrieb"]/text()').extract()
            
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Date,Label) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).encode('utf-8').strip()),
                  escape_string("".join(s).encode('utf-8').strip()),
                  "German Radio Charts",
                  "Germany",
                  "International Radio",
                  escape_string("".join(ranks[index]).encode('utf-8').strip()),
                  now,
                  escape_string("".join(label_1[index]).encode('utf-8').strip()+" ("+"".join(label_2[index]).encode('utf-8').strip()+")" ),
                  
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1

        if source=="Radio Callouts":
            chart_name=response.meta['chart_name']

            ranks=sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[1]/span/text()').extract()
            artists=sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[2]/span/text()').extract()
            songs=sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[3]/span/text()').extract()
            labels=sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[4]/span/text()').extract()
            pop_score= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[6]/span/text()').extract()
            potential= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[7]/span/text()').extract()
            pos= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[8]/span/text()').extract()
            fav= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[9]/span/text()').extract()
            neg= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[10]/span/text()').extract()
            net_pos= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[11]/span/text()').extract()
            burn= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[12]/span/text()').extract()
            familiarity= sel.xpath('//*[@class="report"]/table/tr[position()>=2 and not(position()>=10000)]/td[13]/span/text()').extract()
            
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
            
            index=0
            for s in songs:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_type,Rank,Date,Label,pop_score,potential,positives,favorites,negatives,net_positive,burn,familiarity) \
                    values('%s', '%s', '%s','%s', '%s','%s','%s','%s', '%s', '%s','%s', '%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artists[index]).encode('utf-8').strip()),
                  escape_string("".join(s).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  "Radio Callouts",
                  escape_string("".join(ranks[index]).encode('utf-8').strip()),
                  now,
                  escape_string("".join(labels[index]).encode('utf-8').strip()),
                  escape_string("".join(pop_score[index]).encode('utf-8').strip()),
                  escape_string("".join(potential[index]).encode('utf-8').strip()),
                  escape_string("".join(pos[index]).encode('utf-8').strip()),
                  escape_string("".join(fav[index]).encode('utf-8').strip()),
                  escape_string("".join(neg[index]).encode('utf-8').strip()),
                  escape_string("".join(net_pos[index]).encode('utf-8').strip()),
                  escape_string("".join(burn[index]).encode('utf-8').strip()),
                  escape_string("".join(familiarity[index]).encode('utf-8').strip()),
                  
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except Exception,e:
                    raise e

                index=index+1



        CONN.commit()

    # def __init__(self):
    #     dispatcher.connect(self.spider_closed, signals.spider_closed) 

    # def spider_closed(self, spider):
    #     self.driver.quit()       
    # 