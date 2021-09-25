#!/usr/bin/bash

##############################################################
# Program: Running web-scraping Python script spesific date.
# Parameter:
#   - job_date: %Y-%m-%d format (DEFAULT: yesterday)
# Example:
#   sh run_scraper.sh 2021-09-22
##############################################################

##### Variables #####
job_date=$1

if [[ $job_date = '' ]]; then
  echo "job_date wasn't provided. Use default value."
  job_date=`date -d "1 days ago" '+%Y-%m-%d'`
fi

##### Main #####
echo "Running Scraper with date: $job_date"
python /app/web_scraping/scraper/run_scraper.py $job_date

echo "Backup result"
cp /app/web_scraping/result/scraping_result.csv /backup/scraping_result-$job_date.csv

echo "Loading Scraper result to database"
bash /app/web_scraping/loader/run_loader.sh
rm /app/web_scraping/result/scraping_result.csv

exit 0
