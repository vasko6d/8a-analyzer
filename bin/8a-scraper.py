from bs4 import BeautifulSoup
import requests
import html5lib
import datetime
import re
import os.path
import json
import argparse
from vars import currentGradeMap, currentAscentTypeMap, recommendMap, areaMaps, headers, ascentStartMarker, ascentEndMarker, stateEquivalences

# Helpful Google Links:
# https://stackoverflow.com/questions/34573605/python-requests-get-returns-an-empty-string?rq=1
# https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
# https://www.edureka.co/blog/web-scraping-with-python/

# Prevent multiple of same log statement
hideLog = set()


def standardizeName(name):
    return re.sub("[^A-Z0-9_]", "", re.sub("\s+", "_", name.strip().upper()))


def parseHoverFxnToAreaMap(hoverFxnStr):
    m1 = re.search("encodeURIComponent\('([^']+)", hoverFxnStr)
    m2 = re.findall("\: (.*?(?=<br>|&lt;br&gt;))", m1.group(1))
    divs = m2[1].split(',')
    ret = {
        "country": m2[0],
        "div1": divs[1] if len(divs) > 1 else divs[0] if len(divs) > 0 else "n/a",
        "div2": divs[0] if len(divs) > 0 else "n/a"
    }
    return ret


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
            ascent["area"] = standardizeName(rawArr[0])
            if len(rawArr) == 2:
                ascent["subArea"] = standardizeName(rawArr[1])

            # [4.1] - Country and State / Provence
            areaMap = None
            if ascent["area"] in areaMaps:
                areaMap = areaMaps[ascent["area"]]
            else:
                rawA = tds[4].find('a')
                if rawA:
                    rawHoverFxn = rawA.attrs['onmouseover']
                    areaMap = parseHoverFxnToAreaMap(rawHoverFxn)
            # If we dont have an area map
            if areaMap:
                ascent["country"] = areaMap["country"]
                if areaMap["div1"] in stateEquivalences:
                    ascent["state"] = stateEquivalences[areaMap["div1"]]
                else:
                    ascent["state"] = areaMap["div1"]
                ascent["city"] = areaMap["div2"]
            else:
                logkey = "COUNTRY:DNE:" + ascent["area"]
                if logkey not in hideLog:
                    print(
                        "\t> [WARN - COUNTRY]: Crag [{}] does not have a valid area to Location Map so Country and State not found".format(ascent["area"]))
                    hideLog.add(logkey)

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
