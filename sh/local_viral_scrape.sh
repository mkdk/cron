#!/bin/bash

cd '//var/www/vhosts/island-research.com/cron/local_viral_scrape'

scrapy crawl music -s LOG_FILE=/var/www/vhosts/island-research.com/cron/out_cron
