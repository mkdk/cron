# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class MusicItem(scrapy.Item):
	# Shazam.com

	# Rank=scrapy.Field()
	# Song=scrapy.Field()
	# Artist=scrapy.Field()
	# No_of_Shazams=scrapy.Field()
	# Url=scrapy.Field()

	# Itunes Rss
	TopHistoricAdds=scrapy.Field()
	NoAdds=scrapy.Field()
	PeakRank=scrapy.Field()
	Rank=scrapy.Field()
	Followers=scrapy.Field()
	ChartName=scrapy.Field()
	Song=scrapy.Field()
	Album=scrapy.Field()
	Artist=scrapy.Field()
	Genre=scrapy.Field()
	Price=scrapy.Field()
	Release_Date=scrapy.Field()
	Label=scrapy.Field()
	Url=scrapy.Field()
	No_of_Blogs_Posted=scrapy.Field()
	Spins_1=scrapy.Field()
	Spins_2=scrapy.Field()
	SpinsMove=scrapy.Field()
	Audience=scrapy.Field()
	AudienceMove=scrapy.Field()
	