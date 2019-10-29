# 8a.nu Scraper and Analyzer 
**w/ Python (BeautifulSoup4 + Requests)**

If you are a regular climbing junkie chances are you have at least heard of 8a.nu. If you HAVE heard of 8a.nu, and you have had the privledge of using it.... well, lets just say you know it has a steep learning curve...

For those of you who have never heard of or used 8a.nu, it is a website where people track their rock climbing over time. Every time you "send" a boulder or route (succesfully climb it), you log it on this website. It is super nice for tracking reasons, and since there is a large enough user base, it is incredibly useful for finding popular and quality climbs at a crag. It does not help you literally find climbs like Mountain Project, but because many more people long their sends on 8a.nu it is a much better set of data for seing what climbs people actually do, which climbs are "soft" (or easy), and which climbs people like

## Goal

To make a simple set of tools to:
- [x] Scrape 8a data - initially just scorecards, but specific climbs or crags could prove fruitful.
- [x] Save scraped data locally - if the internet dies you dont want to lose your ticklist! Its seriously become my diary. Ive probably spent 100s of hours logging over the years so it is rather sentimental. Nice for peace of mind to know i have a ".json" or a ".csv"
- [ ] Analyze that data - 8a has all the data, but I often want to look at my data in various ways... like "What day did I climb the most climbs?", "What day did I climb the hardest things", "how many climbs have I climbed in Tramway?". These relatively simple queries would be trivial with database access, but there is no way to do it in the 8a.nu UI. 


## Setup 
* Make sure you have Python 3 installed
* Clone or download repository
* ```pip3 install -r requirements.txt```
* Scrape away dear boy!
```
jens@mac128k~/spaghetti-code$ python3 bin/8a-scraper.py --help
usage: 8a-scraper.py [-h] [--tmpFile TMPFILE] [--outFile OUTFILE]
                     [--delimiter DELIMITER]
                     URL

Scrape 8a and write your scorecard to delimited file

positional arguments:
  URL                   8a.nu bouldering scorecard to scrape. NOTE: URL MUST
                        have the GID=##### parameter

optional arguments:
  -h, --help            show this help message and exit
  --tmpFile TMPFILE     An intermediate file for write/read. If the file does
                        not exist program will scrape given URL and save the
                        HTML as indicated file. If the file does exist,
                        program will read specified file assuming it is the
                        scraped HTML. If no file is specitied URL will be read
                        and scraped all in memory. EXAMPLE >>python3
                        8a-scraper.py --delimiter "|" --tmpFile dv-
                        scorecard3.html "https://www.8a.nu/scorecard/david-vas
                        ko/boulders/?AscentClass=0&AscentListViewType=0&GID=d9
                        6e250ee9136da4105514a70e6e38e8"
  --outFile OUTFILE     The delimited file that will be written to, each line
                        with an ascent. DEFAULT: "8aScrape.out"
  --delimiter DELIMITER
                        out file delimiter. if this is [json] will write as
                        json. DEFAULT: "|"
```

### Notes:
Remember that when web-scraping, any web-site (especially a seemingly spaghetti like one like 8a) has a fairly high chance of changing in subtle ways that can easily break your scraper. Personally, I look directly for a comment ```<!-- ASCENTS -->``` to know where the Ascents table starts. If this comment is removed... well the scraper is broken. I also use a dict for transforming uglified function names to the appropriate v-grade (e.g. "A8_ea3a0c3e0e84736e61d7b4ae4aa07145()": "10"). I assume once 8a.nu is updated in ANY way this function name will change and I will have to update my uglyGradeMap. 
