from bs4 import BeautifulSoup
import requests
import html5lib
import datetime
import re
import os.path
import json
import argparse

# Helpful Google Links:
# https://stackoverflow.com/questions/34573605/python-requests-get-returns-an-empty-string?rq=1
# https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
# https://www.edureka.co/blog/web-scraping-with-python/

# Personal 8a Link
my8aURL = "https://www.8a.nu/scorecard/david-vasko/boulders/?AscentClass=0&AscentListViewType=0&GID=d96e250ee9136da4105514a70e6e38e8"

#
# 8a Specific Scraping Variables (high chance of changing)
#
ascentStartMarker = "<!-- Ascents -->"
ascentEndMarker = "</table>"
currentGradeMap = {
    "A8_8a2f2ba201c69c72f5fae6d5b490ca31()": "15",
    "A8_371ada172e6aca6d36030cff991c2110()": "14",
    "A8_70ae3987db297649adfa22ec835bbef5()": "13",
    "A8_f94c1a7c1ade88cfeb2bd73ffa116d9f()": "12",
    "A8_59b85d692c593f314ed49d15870ff8d2()": "11",
    "A8_ea3a0c3e0e84736e61d7b4ae4aa07145()": "10",
    "A8_2d8a2dca8da8f8595bfafa25580f88c4()": "9",
    "A8_ebe1c7b6a0324f26fa1203e423827d73()": "8",
    "A8_a3ef9ab41d342fca7c6d3bf3b2e01ca2()": "7/8",
    "A8_b68c76e55910e67faca8829b4700d2e1()": "7",
    "A8_728a1685254b76fb0532dd2bd83fc670()": "6",
    "A8_323b60c5b47a45c73f666867fd27b319()": "5/6",
    "A8_59ed716391fbf46727ad091b93b1b507()": "5",
    "A8_8e761f5120d8a81b268c721eb940f633()": "4/5",
    "A8_4b0680d2e6545260c512c8424e7d0180()": "4",
    "A8_31d055ac30224e9cb434b74b6f77c9fe()": "3/4",
    "A8_3cd6d35aa8f427f02d106c1c40969227()": "3",
    "A8_b69a020c915c748aba94ed6c86226541()": "2",
    "A8_10d988d607dfa42c867b638336965a99()": "1",
    "A8_217b0d256645bca88490d2f8257ffecd()": "0",
    "A8_027540acd8eb24681172603ebf359a5c()": "B",
    "A8_5e6e11644ad74bc7fa3554dc12d16d5d()": "B",
    "A8_d02544d610dbfd7bb34cb85ff612365c()": "B"

}
currentAscentTypeMap = {
    "/scorecard/images/56f871c6548ae32aaa78672c1996df7f.gif": "flash",
    "/scorecard/images/979607b133a6622a1fc3443e564d9577.gif": "redpoint",
    "/scorecard/images/e37046f07ac72e84f91d7f29f8455b58.gif": "onsite"
}
recommendMap = {
    "/scorecard/images/UserRecommended_1.gif": True,
    "/scorecard/images/UserRecommended_0.gif": False
}
# Headers from inspecting te desired request on 8a.nu directly
headers = {
    "Host": "www.8a.nu",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://www.8a.nu/user/My8a.aspx",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}


def standardizeAreaName(name):
    return re.sub("\s+", "_", name.strip().upper())


def scrapeBoulderScorecare(a8URL):
    # Get the raw HTML for the specified URL and return it as a bs4 soup object
    print("Starting 8a scrape")
    with requests.Session() as session:

        print("\tGetting 8a.nu session.......")
        session.headers = headers
        sr = session.get("https://www.8a.nu", timeout=60)
        print("\t   ...done: {}".format(sr))

        print("\tGetting ticklist from 8a.....")
        r = session.get(a8URL, timeout=60)
        print("\t   ...done {}".format(r))

        return str(BeautifulSoup(r.content, "html5lib"))


def processAscent(htmlRow):
    tds = htmlRow.find_all("td")

    # Specify a minimum length to omit junk(empty) rows
    if len(tds) > 2:
        try:
            ascent = {}

            # [0] - Date
            rawStr = tds[0].text
            rawStr = rawStr[len(rawStr)-8:]
            date = datetime.datetime.strptime(rawStr, "%y-%m-%d")
            ascent["date"] = date

            # [1] - Ascent Type: redpoint, flash or onsite
            rawStr = tds[1].img['src']
            ascent["type"] = currentAscentTypeMap[rawStr]

            # [2] - Climb Name
            rawStr = tds[2].a.text.strip()
            ascent["name"] = rawStr

            # [3] - Reccommend?
            rawStr = tds[3].img['src']
            ascent["recommend"] = recommendMap[rawStr]

            # [4] - Area and sub area
            rawStr = tds[4].text
            rawArr = rawStr.split("/", 1)
            ascent["area"] = standardizeAreaName(rawArr[0])
            if len(rawArr) == 2:
                ascent["subArea"] = standardizeAreaName(rawArr[1])

            # [5] - Flags
            rawStr = tds[5].contents[0]
            rawArr = rawStr.split(",")
            ascent["flags"] = []
            for el in rawArr:
                if el.strip():
                    ascent["flags"].append(el.strip())
            # also add flash or onsigth as flag
            if ascent["type"] == "flash" or ascent["type"] == "onsite":
                ascent["flags"].append(ascent["type"])

            # [6] - Comment (first remove the starting span)
            raw = str(tds[6])
            start = raw.find("</span>") + len("</span>")
            end = raw.find("</td>")
            comment = raw[start:end]
            leadingSpaces = len(comment) - len(comment.lstrip(" "))
            if leadingSpaces > 0:
                spaceStr = comment[0:leadingSpaces]
                comment = comment.replace(spaceStr, "")
            comment = comment.replace("\n<br/>", "").rstrip()
            ascent["comment"] = comment
            ascent["commentLength"] = len(comment)

            # [7] - Stars
            rawStr = tds[7].contents[0]
            starCount = rawStr.count("*")
            ascent["rating"] = starCount

            return ascent
        except Exception as e:
            print("[Error] error occured parsing the following HTML:\n{}\n[exception] {}".format(
                htmlRow, str(e)))


def processHeaderRow(htmlRow):
    grade = None
    gradeHeader = row.find_all("td", {"class": "AscentListHeadRow"})
    if gradeHeader:
        uglyGradeFunction = gradeHeader[0].b.script.text.strip()
        grade = currentGradeMap[uglyGradeFunction]
    return grade


def delimitAscent(ascent, delimiter):
    sb = []
    sb.append(str(ascent['date'].strftime('%Y-%m-%d')))
    sb.append(str(ascent['name']))
    sb.append(str(ascent['grade']))
    sb.append(str(ascent['rating']))
    sb.append(str(ascent['recommend']))
    sb.append(str(ascent['area']))
    if'subArea' in ascent:
        sb.append(str(ascent['subArea']))
    else:
        sb.append('')
    sb.append(str(ascent['type']))
    sb.append(str(ascent['flags']))
    sb.append(str(ascent['comment']))
    return delimiter.join(sb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrape 8a and write your scorecard to delimited file')
    parser.add_argument(
        'URL', type=str, help='8a.nu bouldering scorecard to scrape. NOTE: URL MUST have the GID=##### parameter')
    parser.add_argument('--tmpFile', type=str,
                        help='An intermediate file for write/read. If the file' +
                        ' does not exist program will scrape given URL and save' +
                        ' the HTML as indicated file. If the file does exist,' +
                        ' program will read specified file assuming it is the' +
                        ' scraped HTML. If no file is specitied URL will be' +
                        ' read and scraped all in memory. EXAMPLE\n>>python3 8a-scraper.py --delimiter "|" --tmpFile dv-scorecard3.html "https://www.8a.nu/scorecard/david-vasko/boulders/?AscentClass=0&AscentListViewType=0&GID=d96e250ee9136da4105514a70e6e38e8"')
    parser.add_argument('--outFile', type=str, default='8aScrape.out',
                        help='The delimited file that will be written to, each line with an ascent. DEFAULT: "8aScrape.out"')
    parser.add_argument('--delimiter', default='|', type=str,
                        help='out file delimiter. if this is [json] will write as json. DEFAULT: "|"')
    args = parser.parse_args()

    raw = None
    writeTmpFile = True
    if args.tmpFile:
        if os.path.exists(args.tmpFile):
            f = open(args.tmpFile, 'r')
            raw = f.read()
            f.close()
            writeTmpFile = False

    if not raw:
        raw = scrapeBoulderScorecare(args.URL)

    if args.tmpFile and writeTmpFile:
        print("\tWriting tmp file [{}].....".format(args.tmpFile))
        f = open(args.tmpFile, 'w')
        f.write(raw)
        f.close()
        print("\t   ...done")

    # Manually Trim Raw to encapsulate the desired ,TABLE which as of now is indicated most easily by a comment <!-- ASCENTS -->
    print("\tProcessing Beautiful Soup of 8a...")
    start = raw.find(ascentStartMarker) + len(ascentStartMarker) + 1
    end = raw.find(ascentEndMarker, start, len(raw)) + len(ascentEndMarker)
    soup = BeautifulSoup(raw[start:end], "html5lib")

    # Iterate yours soup!
    curGrade = -1
    cnt = {'total': 0}
    of = open(args.outFile, 'w')
    if args.delimiter == 'json':
        of.write('{ "ascents": [\n')
    else:
        of.write(args.delimiter.join(['date', 'name', 'grade', 'rating',
                                      'recommend', 'area', 'subArea', 'type', 'flags', 'comment']))
    rows = soup.find_all("tr")
    for i, row in enumerate(rows):
        newGrade = processHeaderRow(row)
        if(newGrade):
            curGrade = newGrade
        else:
            ascent = processAscent(row)
            if ascent:
                ascent["grade"] = curGrade
                if args.delimiter == 'json':
                    ascent['date'] = ascent['date'].strftime('%Y-%m-%d')
                    of.write('\t')
                    of.write(json.dumps(ascent))
                    if i < len(rows) - 1:
                        of.write(',')
                else:
                    of.write(delimitAscent(ascent, args.delimiter))
                of.write('\n')
                if curGrade in cnt:
                    cnt[curGrade] += 1
                else:
                    cnt[curGrade] = 1
                cnt['total'] += 1
    if args.delimiter == "json":
        of.write("]\n}")
    of.close()
    print("\t   ...done")
    print("Total Climbs Scraped: [{}]".format(cnt['total']))
    for k in cnt:
        if k != 'total':
            print("\t> {}: [{}]".format(k, cnt[k]))
