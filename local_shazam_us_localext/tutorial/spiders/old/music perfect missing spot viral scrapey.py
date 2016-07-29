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

         # Spotify viral
        now = datetime.date.today()
        date=now.strftime("%m/%d/%Y")
        
        #self.driver=webdriver.Chrome("chromedriver.exe")
        self.driver=webdriver.Chrome()
        #self.driver=webdriver.Firefox()
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0

       
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
                    #if artist name contains " ," flip first + last name. If it contains "/" or "&", flip for each artist.
                    amp = '';
                    slash = '';
                    if ", " in artist[index]:
                        import unicodedata;
                        artist[index]=unicodedata.normalize('NFKD', artist[index]).encode('ascii','ignore')
                        if "&" in artist[index] or "/" in artist[index]:
                            if "&" in artist[index]:
                                amp = 'Yes';
                            if "/" in artist[index]:
                                slash = 'Yes';           
                            if amp == 'Yes':
                                artist1=artist[index].split("&",1)[0];
                                artist2=artist[index].split("&",1)[1];
                                artist1=str.strip(artist1);
                                artist2=str.strip(artist2);                
                            if slash == 'Yes':
                                artist1=artist[index].split("/",1)[0];
                                artist2=artist[index].split("/",1)[1];
                                artist1=str.strip(artist1);
                                artist2=str.strip(artist2);  
                            if ", " in artist1:
                                sub1artist1=artist1.split(", ",1)[0];
                                sub2artist1=artist1.split(", ",1)[1];
                                artist1=sub2artist1 + " "+ sub1artist1
                            if ", " in artist2:
                                sub1artist2=artist2.split(", ",1)[0];
                                sub2artist2=artist2.split(", ",1)[1];
                                artist2=sub2artist2 + " "+ sub1artist2
                            if amp=="Yes":
                                artist[index]=artist1 + " & " + artist2;
                            if slash=="Yes":
                                artist[index]=artist1 + "/" + artist2;
                        else:
                            sub1artist=artist[index].split(", ",1)[0];
                            sub1artist=str.strip(sub1artist);
                            sub2artist=artist[index].split(", ",1)[1];
                            sub2artist=str.strip(sub2artist);
                            artist[index]=sub2artist + " "+ sub1artist;
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
                    #if artist name contains " ," flip first + last name. If it contains "/" or "&", flip for each artist.
                    amp = '';
                    slash = '';
                    if ", " in artist[index]:
                        import unicodedata;
                        artist[index]=unicodedata.normalize('NFKD', artist[index]).encode('ascii','ignore')
                        if "&" in artist[index] or "/" in artist[index]:
                            if "&" in artist[index]:
                                amp = 'Yes';
                            if "/" in artist[index]:
                                slash = 'Yes';           
                            if amp == 'Yes':
                                artist1=artist[index].split("&",1)[0];
                                artist2=artist[index].split("&",1)[1];
                                artist1=str.strip(artist1);
                                artist2=str.strip(artist2);                
                            if slash == 'Yes':
                                artist1=artist[index].split("/",1)[0];
                                artist2=artist[index].split("/",1)[1];
                                artist1=str.strip(artist1);
                                artist2=str.strip(artist2);  
                            if ", " in artist1:
                                sub1artist1=artist1.split(", ",1)[0];
                                sub2artist1=artist1.split(", ",1)[1];
                                artist1=sub2artist1 + " "+ sub1artist1
                            if ", " in artist2:
                                sub1artist2=artist2.split(", ",1)[0];
                                sub2artist2=artist2.split(", ",1)[1];
                                artist2=sub2artist2 + " "+ sub1artist2
                            if amp=="Yes":
                                artist[index]=artist1 + " & " + artist2;
                            if slash=="Yes":
                                artist[index]=artist1 + "/" + artist2;
                        else:
                            sub1artist=artist[index].split(", ",1)[0];
                            sub1artist=str.strip(sub1artist);
                            sub2artist=artist[index].split(", ",1)[1];
                            sub2artist=str.strip(sub2artist);
                            artist[index]=sub2artist + " "+ sub1artist;
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
                if self.todays_date==0: # monday, finishes monday 7pm
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
                if self.todays_date==1: # tuesday, finishes tuesday at 7pm
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
            if chart_name_2=="USA":
                chart_name_2="United States"
            if chart_name_2=="The World":
                chart_name_2="Global"
            chart_type=response.meta['chart_type']
            index=0
            now = datetime.date.today()
            date=now.strftime("%m/%d/%Y")
        
            for r in rank:
                try:
                    shazams = no_of_shazams[index].encode('utf-8').strip().replace(',','')
                    shazams = int(shazams)
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Shazams,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist[index]).encode('utf-8').strip()),
                  escape_string("".join(song[index]).encode('utf-8').strip()),
                  escape_string("".join(chart_name).encode('utf-8').strip()),
                  escape_string("".join(chart_name_2).encode('utf-8').strip()),
                  escape_string("".join(chart_type).encode('utf-8').strip()),
                  escape_string("".join(r).strip()),
                  shazams,
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