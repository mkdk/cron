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
#import msvcrt
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



class MusicSpider(scrapy.Spider):
   
    name = "music"
    
    start_urls=["http://www.shazam.com"]
    
    global x
    x=CONN.cursor()
   
    def parse(self, response):
        sel=Selector(response)
    
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
            yield Request(l[4],meta={'source':l[0].strip(),'chart_type':l[1],'chart':l[2].strip(),'chart_name':l[3]},callback=self.each_detail)
        
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
        
        now = datetime.datetime.now()
        date=now.strftime("%Y%m%d")
        
        #date="20160325"

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
        yield Request("http://hypem.com/popular/noremix/10000",meta={'source':"HypeM.com",'chart_type':"Hype Machine",'chart':"Song",'chart_name':"Popular Now: No Remixes"},callback=self.each_detail)
        
        ################################################################
        
         # Spotify viral
        now = datetime.datetime.now()
        date=now.strftime("%m/%d/%Y")
        
        #self.driver=webdriver.Chrome("chromedriver.exe")
        self.driver=webdriver.Chrome()
        links=[]
        with open('links.csv') as csvfile:
            reader = csv.reader(csvfile)
            count=0
            for row in reader:
                if len(row[4].strip())!=0 and count!=0 and row[0].strip()=="Spotify Flash Website":
                    links.append(row)
                else:
                    count=count+1
            
            self.driver.get("https://play.spotify.com/")
            try:
                self.driver.find_element_by_id("has-account").click()
                inputElement = self.driver.find_element_by_id("login-usr")
                inputElement.send_keys("island1234")
                inputElement = self.driver.find_element_by_id("login-pass")
                inputElement.send_keys("island123")
                inputElement.submit()
            except:
                pass
            
            time.sleep(2)
            
            chart_type="Spotify Viral"
            chart="Song"
            for l in links:

                try:
                    self.driver.get(l[4])
                    #time.sleep(10)
                    wait = WebDriverWait(self.driver, 180)
                        # wait for iframe to become visible
                    iframe = wait.until(EC.visibility_of_element_located((By.XPATH, "//iframe[starts-with(@id, 'browse-app-spotify:app:chart:')]")))
                    self.driver.switch_to.frame(iframe)
                            # wait for header in the container to appear
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main-container #header")))
                    container = self.driver.find_element_by_id("main-container")
                    
                    sel=Selector(text=self.driver.page_source)

                    ranks=sel.xpath('//*[@class="tl-number-wrap"]')
                    songs=sel.xpath('//*[@class="tl-highlight "]')
                    artists=sel.xpath('//*[@class="tl-cell tl-artists"]')
                    albums=sel.xpath('//*[@class="tl-cell tl-albums"]')
                    followers=sel.xpath('//*[@data-bind="text: numFollowersFormatted"]/text()').extract()
                    chart_name=sel.xpath('//*[@class="h-title"]/text()').extract()
                    if len("".join(chart_name))<=0:
                        chart_name=sel.xpath('//*[@data-ta-id="header-name"]/text()').extract()
                        if len("".join(chart_name))<=0:
                            chart_name=l[3]

                    index=0
                    for r in ranks:
                        rank=r.xpath('text()').extract()
                        song=songs[index].xpath('text()').extract()
                        artist=artists[index].xpath('a/text()').extract()
                        if len("".join(albums))>0:
                            album=albums[index].xpath('/a/text()').extract()
                        followers="".join(followers).strip()
                        
                        try:
                            sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_type,Rank,Date) \
                            values('%s', '%s', '%s', '%s','%s','%s')" % ("songs_chart",
                          escape_string(", ".join(artist).encode('utf-8').strip()),
                          escape_string("".join(song).encode('utf-8').strip()),
                          escape_string("".join(chart_name).encode('utf-8').strip()),
                          escape_string("".join(chart_type).encode('utf-8').strip()),
                          escape_string("".join(rank).strip()),
                          "".join(date),
                          )

                            global x
                            if x.execute(sql):
                                print "item Inserted"
                            else:
                                print "Something wrong"
                        except:
                            pass
                        
                        index=index+1

                except:
                    pass

       
        #mediabase

        self.driver.get("http://www.mediabase.com/")
        inputElement = self.driver.find_element_by_name("userName")
        inputElement.send_keys("IDJMG258")
        inputElement = self.driver.find_element_by_name("password")
        inputElement.send_keys("Dmassey")
        inputElement.submit()
        time.sleep(2)
        mbhpage2="http://www.mediabase.com/weblogon/ValidateLogonMIS.asp?UserName=SonyATV21&Password=pacciarito"
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

            if l[1]=="Published Radio":
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
                      "".join(date),
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
                      "".join(date),
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

                title=sel.xpath('//*[@class="Title"][1]/text()').extract()
                subtitle=sel.xpath('//*[@class="subtitlelink"][position()>=1 and not (position()>=2)]/a/text()').extract()
                chart_name="".join(title).strip() +" " +" ".join(subtitle).strip()
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
                      "".join(date),
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
                      "".join(date),
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

        # spotify playlists (API)
        # def show_tracks(results):
        #     for i, item in enumerate(tracks['items']):
        #         track = item['track']
        #         listy = [track['artists'][0]['name'],track['name'],track['album']['name'],i+1]
        #         spotifylist.append(listy)
                
        # SPOTIPY_CLIENT_ID='cd1b9757c8fb44d3958778b5fc999a27'
        # SPOTIPY_CLIENT_SECRET='d7a51913b6994b0ab57f45382fbd30b0'
        # SPOTIPY_REDIRECT_URI='https://www.google.com'
        # scope = 'user-library-read'
        
        # username = 'island1234'
        # token = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        # # if it expires, spotify will direct u to a url and ask you to enter the url you were directed to - follow those instructions and carry on to next parts of this code!
        # # if THAT doesnt work, go to https://developer.spotify.com/web-api/console/get-playlists/ & manually generate token (user library read) & put in below
        # # token = "BQDBi85nJJ1WCW5fv_TcEgwmY-kB1cNB9nrHC3ICqPHnGwsyLylCYKsZ4S8g_St5zY8V_YdwsacbanwPLw4mai2A2R5NibZzDDUSLzyX5CTooQRcGYfQ886KUjfkBpEQQLo7v1iVsIt5yyGVQDsC-rnQU3OwSMFTqHje6ts"
        # sp = spotipy.Spotify(auth=token)
        
        # username2 = 'lmljoe'
        # token2 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        # #token2 = "BQDjeU8dZTKjsKK-AOr3geNCqSByoMm-ABFanKN-NmuRBNcymGF8EfANCV_B1AozABljJMB9lBMZOiVx2podMwiQxn6WzLFej0OBGlkH5dD291nZFYhjFvuVni0OWuw1fKeu9G6PtEyz9ER4w7ibOhKbvSLQTgnkLLCHT-g"
        # sp2 = spotipy.Spotify(auth=token2)
        
        # username3 = 'myplay.com'
        # token3 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        # #token3 = "BQAirwgjE1A-DojGah0RzpCuXUjarC5WMSBAhsX9jD8Zcibuo5pBzVdCO_GOSqNYpmU-_fqXPS4ORswrKG7x1UzOLNqXhk60kdq_2ovVIvikKFDTUxNxHaf-uHAI3OY6-esZ8nJt2d8MX55kiaESRMx2aDbSLUwtrM_2DiQ"
        # sp3 = spotipy.Spotify(auth=token3)
        
        # username4 = 'digster.fm'
        # token4 = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        # #token4 = "...."
        # sp4 = spotipy.Spotify(auth=token4)
        
        ####Spotify-Curated Playlists####
        #Today's Top Hits Spotify Playlist
        # id = '5FJXhjdILmRA2z5bvz4nzf'
        # TopHitsPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = TopHitsPlaylist['tracks']
        # TopHitsPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # self.show_tracks(tracks)
        # TopHitsPlaylist = spotifylist
        
        # print TopHitsPlaylist

        # #Girls' Night Spotify Playlist
        # id = '7uDoSz5VxK5lbXgj7tBMG9'
        # GirlsNightPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = GirlsNightPlaylist['tracks']
        # GirlsNightPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # GirlsNightPlaylist = spotifylist
        
        # #Fresh Finds Spotify Playlist
        # id = '3rgsDhGHZxZ9sB9DQWQfuf'
        # FreshFindsPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = FreshFindsPlaylist['tracks']
        # FreshFindsPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # FreshFindsPlaylist = spotifylist
        
        # #Viral Hits Spotify Playlist
        # id = '2qTeRwnwFquJUKrAFWnolb'
        # ViralHitsPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = ViralHitsPlaylist['tracks']
        # ViralHitsPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # ViralHitsPlaylist = spotifylist
        
        # #Mood Booster Spotify Playlist
        # id = '6uTuhSs7qiEPfCI3QDHXsL'
        # MoodBoosterPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = MoodBoosterPlaylist['tracks']
        # MoodBoosterPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # MoodBoosterPlaylist = spotifylist
        
        # #Top 100 Alternative Tracks Playlist
        # id = '3jtuOxsrTRAWvPPLvlW1VR'
        # TopAltSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = TopAltSpotPlaylist['tracks']
        # TopAltSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # TopAltSpotPlaylist = spotifylist
        
        # #Top 100 Indie Tracks on Spotify Playlist
        # id = '4dJHrPYVdKgaCE3Lxrv1MZ'
        # TopIndieSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = TopIndieSpotPlaylist['tracks']
        # TopIndieSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # TopIndieSpotPlaylist = spotifylist
        
        # #Top 100 Pop Tracks on Spotify Playlist
        # id = '3ZgmfR6lsnCwdffZUan8EA'
        # TopPopSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = TopPopSpotPlaylist['tracks']
        # TopPopSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # TopPopSpotPlaylist = spotifylist
        
        # #Top Tracks in the United States Spotify Playlist
        # id = '6LBZwjKY0VZLoe79qeGcCF'
        # TopTracksUSSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = TopTracksUSSpotPlaylist['tracks']
        # TopTracksUSSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # TopTracksUSSpotPlaylist = spotifylist
        
        # #New Music Friday Spotify Playlist
        # id = '1yHZ5C3penaxRdWR7LRIOb'
        # NewMusicFriPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = NewMusicFriPlaylist['tracks']
        # NewMusicFriPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # NewMusicFriPlaylist = spotifylist
        
        # #Top 100 Tracks Currently on Spotify Playlist
        # id = '4hOKQuZbraPDIfaGbM3lKI'
        # Top100SpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = Top100SpotPlaylist['tracks']
        # Top100SpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # Top100SpotPlaylist = spotifylist
        
        # #Hot Alternative Spotify Playlist
        # id = '2YoVrFsJPvunjHQYfM12cP'
        # HotAltSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = HotAltSpotPlaylist['tracks']
        # HotAltSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # HotAltSpotPlaylist = spotifylist
        
        # #The Indie Mix Spotify Playlist
        # id = '75dwLdmL07hDEDWqX17QeE'
        # IndieMixSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = IndieMixSpotPlaylist['tracks']
        # IndieMixSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # IndieMixSpotPlaylist = spotifylist
        
        # #Indie Pop! Spotify Playlist
        # id = '2ikvjqFDwalfKdCHkxn79O'
        # IndiePopSpotPlaylist = sp.user_playlist(username, playlist_id=id, fields="tracks,next")
        # tracks = IndiePopSpotPlaylist['tracks']
        # IndiePopSpotPlaylistFollowers = sp.user_playlist(username, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # IndiePopSpotPlaylist = spotifylist
        
        # ####lmljoe-Curated Playlists####
        
        # #Acoustic Lounge Spotify Playlist
        # id = '0DXoY83tBvgWkd8QH49yAI'
        # AcousticLoungeSpotPlaylist = sp2.user_playlist(username2, playlist_id=id, fields="tracks,next")
        # tracks = AcousticLoungeSpotPlaylist['tracks']
        # AcousticLoungeSpotPlaylistFollowers = sp.user_playlist(username2, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # AcousticLoungeSpotPlaylist = spotifylist
        
        # ####myplay.com-Curated Playlists####
        
        # #Top of the Charts Spotify Playlist
        # id = '4ANVDtJVtVMVc2Nk79VU1M'
        # TopOfChartsSpotPlaylist = sp3.user_playlist(username3, playlist_id=id, fields="tracks,next")
        # tracks = TopOfChartsSpotPlaylist['tracks']
        # TopOfChartsSpotPlaylistFollowers = sp.user_playlist(username3, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # TopOfChartsSpotPlaylist = spotifylist
        
        # ####digster.fm-Curated Playlists####
        
        # #Hits Spotify Playlist
        # id = '4noDy1IQejcxDbTLvzuWhS'
        # HitsDigsterSpotPlaylist = sp4.user_playlist(username4, playlist_id=id, fields="tracks,next")
        # tracks = HitsDigsterSpotPlaylist['tracks']
        # HitsDigsterSpotPlaylistFollowers = sp.user_playlist(username4, playlist_id=id, fields="followers")['followers']['total']
        # spotifylist=list()
        # show_tracks(tracks)
        # HitsDigsterSpotPlaylist = spotifylist
        
    def each_detail(self,response):
        #open_in_browser(response)
        sel=Selector(response)
        # shazam

        source=response.meta['source']

        if source=="Shazam.com":
            sel=Selector(response)
            rank=sel.xpath('//*[@itemprop="track"]/@data-chart-position').extract()
            song=sel.xpath('//*[@class="ti__title"]/a/text()').extract()
            artist=sel.xpath('//*[@class="ti__artist"]/meta/@content').extract()
            no_of_shazams=sel.xpath('//*[@class="ti__tagcount"]/span/text()').extract()
            temp_1=sel.xpath('//*[@class="chrt-nav__select__details"][1]/text()').extract()
            temp_2=sel.xpath('//*[@class="chrt-nav__select__details"][2]/text()').extract()
            chart_name="".join(temp_1).strip()
            chart_name_2="".join(temp_2).strip()
            chart_type=response.meta['chart_type']
            index=0
            now = datetime.datetime.now()
            date=now.strftime("%m/%d/%Y")
        
            for r in rank:
                try:
                    sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Shazams,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist[index]).encode('utf-8')),
                  escape_string("".join(song[index]).encode('utf-8')),
                  escape_string("".join(chart_name).encode('utf-8')),
                  escape_string("".join(chart_name_2).encode('utf-8')),
                  escape_string("".join(chart_type)).encode('utf-8'),
                  escape_string("".join(r)),
                  escape_string("".join(no_of_shazams[index]).encode('utf-8')),
                  "".join(date),
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

            now = datetime.datetime.now()
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
                    temp="".join(chart_name).split()[0]
                    chart_name_2="".join(chart_name).split()[1].replace('(','').replace(')','').strip()

                    if chart=="Song":
                        sql = "INSERT INTO %s (Artist,Song,Chart_name,Chart_name_2,Chart_type,Rank,Album,Price,Genre,ReleaseDate,Label,Date) \
                        values('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ("songs_chart",
                      escape_string(artist.encode('utf-8')),
                      escape_string(song.encode('utf-8')),
                      escape_string(temp.encode('utf-8')),
                      escape_string(chart_name_2.encode('utf-8')),
                      escape_string(chart_type.encode('utf-8')),
                      escape_string(str(rank)),
                      escape_string(album.encode('utf-8')),
                      escape_string(price.encode('utf-8')),
                      escape_string(genre.encode('utf-8')),
                      escape_string(release_date),
                      escape_string("".join(final_label).encode('utf-8').strip()),
                      "".join(date),
                      )

                        global x
                        if x.execute(sql):
                            print "item Inserted"
                        else:
                            print "Something wrong"

                    elif chart=="Album":
                        sql = "INSERT INTO %s (Artist,Chart_name,Chart_name_2,Chart_type,Rank,Album,Price,Genre,ReleaseDate,Label,Date) \
                        values('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ("album_chart",
                      escape_string(artist.encode('utf-8')),
                      escape_string(temp.encode('utf-8')),
                      escape_string(chart_name_2.encode('utf-8')),
                      escape_string(chart_type.encode('utf-8')),
                      escape_string(str(rank)),
                      escape_string(song.encode('utf-8')),
                      escape_string(price.encode('utf-8')),
                      escape_string(genre.encode('utf-8')),
                      escape_string(release_date),
                      escape_string("".join(final_label).encode('utf-8').strip()),
                      "".join(date),
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

            now = datetime.datetime.now()
            date=now.strftime("%m/%d/%Y")
        
            with open("temp.json") as json_file:
                json_data = json.load(json_file)
                total_results=json_data["chart"]

                rank=1

                for t in total_results:
                    song=t["heading"]["title"]
                    artist=t["heading"]["subtitle"]
                    
                    try:
                        sql = "INSERT INTO %s (Artist,Song,Chart_name,chart_name_2,Chart_type,Rank,Date) \
                    values('%s', '%s', '%s', '%s','%s','%s','%s')" % ("songs_chart",
                  escape_string("".join(artist).encode('utf-8')),
                  escape_string("".join(song).encode('utf-8')),
                  escape_string("US Local"),
                  escape_string("".join(chart_name).encode('utf-8')),
                  escape_string("".join(chart_type).encode('utf-8')),
                  escape_string(str(rank)),
                  "".join(date),
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

            now = datetime.datetime.now()
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
                  escape_string(artist.encode('utf-8')),
                  escape_string(song.encode('utf-8')),
                  escape_string(chart_name.encode('utf-8')),
                  escape_string(chart_type.encode('utf-8')),
                  escape_string(str(rank)),
                  "".join(date),
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

            now = datetime.datetime.now()
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
                  escape_string("".join(temp_artist).encode('utf-8')),
                  escape_string("".join(temp_song).encode('utf-8')),
                  escape_string("".join(chart_name).encode('utf-8')),
                  escape_string("".join(chart_type).encode('utf-8')),
                  escape_string("".join(temp_rank).encode('utf-8')),
                  escape_string("".join(temp_blog).encode('utf-8')),
                  "".join(date),
                  )

                    global x
                    if x.execute(sql):
                        print "item Inserted"
                    else:
                        print "Something wrong"

                except:
                    pass
                    

        CONN.commit()

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed) 

    def spider_closed(self, spider):
        self.driver.quit()       
    