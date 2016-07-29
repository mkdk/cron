#!/bin/bash

cd '/var/www/vhosts/island-research.com/cron/local_shazam_us_local'

scrapy crawl music -s LOG_FILE=/var/www/vhosts/island-research.com/cron/out_cron
