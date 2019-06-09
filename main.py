import Crawler as c
import pandas as pd
import os
from datetime import datetime
import time

crawler = c.Crawler()
crawler.crawl()

df = pd.DataFrame()
count = 1
print("Start merging..")
for i in os.listdir("./raw/"):
    print(str(count) + ". file: " + str(i))
    count += 1
    df = df.append(pd.read_csv("./raw/" + str(i), sep=";", encoding="utf-8", decimal=","), sort=False)

df = df.drop_duplicates(subset="URL")

succ = df.to_csv('./data/' + str(datetime.now())[:19].replace(':', '').replace('.', '') + '.csv',
          sep=';', decimal=',', encoding='utf-8', index_label='timestamp')

if succ:
    now = time.time()
    # deleting merges older than 3 days
    for f in os.listdir('./data/'):
        path = os.path.join('./data/', f)
        if os.stat(path).st_mtime < now - 7 * 86400:
            os.remove(path)

    # deleting raw data older than 14 days
    for f in os.listdir('./raw/'):
        path = os.path.join('./raw/', f)
        if os.stat(path).st_mtime < now - 14 * 86400:
            os.remove(path)