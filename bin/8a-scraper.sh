#!/bin/bash
# Helpful Link: https://unix.stackexchange.com/questions/82598/how-do-i-write-a-retry-logic-in-script-to-keep-retrying-to-run-it-upto-5-times
for cmnd in \
    'python3 bin/8a-scraper.py --delimiter "json" --tmpFile david-vasko.html --outFile david-vasko.json "https://www.8a.nu/scorecard/david-vasko/boulders/?AscentClass=0&AscentListViewType=0&GID=d96e250ee9136da4105514a70e6e38e8"' \
    'python3 bin/8a-scraper.py --delimiter "json" --tmpFile chase-yamashiro.html --outFile chase-yamashiro.json "https://www.8a.nu/scorecard/alan-nalitch/boulders/?AscentClass=0&AscentListViewType=0&GID=30c1309390fb08b4e14529d75fde901b"' \
    'python3 bin/8a-scraper.py --delimiter "json" --tmpFile daniel-fong.html --outFile daniel-fong.json "https://www.8a.nu/scorecard/fanny-dong/boulders/?AscentClass=0&AscentListViewType=0&GID=f69b2e68070744bfd298dd60f76dcb5f"' \
    'python3 bin/8a-scraper.py --delimiter "json" --tmpFile scott-baron.html --outFile scott-baron.json "https://www.8a.nu/scorecard/dirk-irector/boulders/?AscentClass=0&AscentListViewType=0&GID=a03bc066b057a4812722a15035a58bad"' \
    'python3 bin/8a-scraper.py --delimiter "json" --tmpFile nathaniel-cushing-murray.html --outFile nathaniel-cushing-murray.json "https://www.8a.nu/scorecard/chris-rush/boulders/?AscentClass=0&AscentListViewType=0&GID=7df805fe7444482ff3cfd8ecd38aaace"' \
    'python3 bin/8a-scraper.py --delimiter "json" --tmpFile drew-gomberg.html --outFile drew-gomberg.json "https://www.8a.nu/scorecard/chris-hoss/boulders/?AscentClass=0&AscentListViewType=0&GID=72bb5f75dad248435df3bf295f1c0964"'; \
    do
    for i in $(seq 1 5); do 
        [ $i -gt 1 ] && sleep 15; 
        echo "[$i] - attempt at command: $cmnd"
        eval $cmnd  && s=0 && break || s=$?; 
    done; 
    (exit $s)
done;