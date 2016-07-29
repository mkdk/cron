# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import datetime

class TutorialPipeline(object):

  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = open("mediabase.csv", 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    #self.exporter.fields_to_export = ["Name","Address","City","Neighborhood","State","Zip","Phone","Website","Image_url","Hours_Mon","Hours_Tue","Hours_Wed","Hours_Thu","Hours_Fri","Hours_Sat","Hours_Sun","Price","TakesReservation","Delivery","TakeOut","AcceptsCreditCards","GoodFor","Parking","WheelChairAccessible","BikeParking","GoodForKids","GoodForGroups","Attire","Ambience","NoiseLevel","Alcohol","OutDoorSeating","Wifi","HasTV","WaiterService","Caters","Url"]
    self.exporter.fields_to_export = ["Type","Area","PlaceName","Web","Tel","Address","Zip","Town","Hours","CompanyName","OrganizationNo","Turnover","Employed","LastName","FirstName","Telephone","AllabolagUrl","EniroUrl"]
    self.exporter.start_exporting()
  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item


# # class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item
