import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
from urllib.parse import urljoin

class Crawler():

    def crawl(self):
        main_url = 'https://www.immobilienscout24.de'
        href = '/Suche/S-T/Garage-Kauf/Bayern/Muenchen'

        df = pd.DataFrame()
        counter = 0

        while href != '':
            print(main_url+href)
            time.sleep(1)
            r = requests.get(main_url+href)
            main_site = BeautifulSoup(r.text, 'html.parser')

            exposes = []
            for p in main_site.find_all('a'):
                if r'/expose/' in str(p.attrs['href']):
                    exposes.append(p.get('href').split('#')[0])

            unique_exposes = list(set(exposes))

            for e_href in unique_exposes:
                time.sleep(0.5)
                r = requests.get(main_url + e_href)
                expose_site = BeautifulSoup(r.text, 'html.parser')
                print(str(counter) + ' ' + expose_site.select('title')[0].text + ' ' + str(e_href))

                data = pd.DataFrame(
                    json.loads(str(expose_site.find_all('script')).split('keyValues = ')[1].split('}')[0] + str('}')),
                    index=[str(datetime.now())])
                data['name'] = expose_site.select('title')[0].text
                data['URL'] = str(main_url+e_href)

                description = []

                for i in expose_site.find_all('pre'):
                    description.append(i.text)

                data['description'] = str(description)

                df = df.append(data, sort=False)
                counter += 1

            df.to_csv('./data/' + str(datetime.now())[:19].replace(':', '').replace('.', '') + '.csv',
                      sep=';', decimal=',', encoding='utf-8', index_label='timestamp')

            next = main_site.select('#pager a')
            # buttons for prev and next page
            if len(next) == 2 :
                href = next[1].attrs['href']
            # start page
            elif len(next) == 1 and str(next[0].attrs['data-is24-qa']) == 'paging_bottom_next':
                href = next[0].attrs['href']
            else:
                print('Final site visited: ' + href)
                href = ''