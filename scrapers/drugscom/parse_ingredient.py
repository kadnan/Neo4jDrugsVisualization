import re
from utils import *
import requests, time, traceback
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
from time import sleep
import random


def get_links(LIMIT=10):
    total_links = []
    _links = []
    try:
        print('Calling')
        sql = 'SELECT DISTINCT(url) from {} WHERE status = 0 LIMIT {}'.format('ingredients', LIMIT)
        cursor = connection.cursor()
        cursor.execute(sql)
        links = cursor.fetchall()
        for link in links:
            total_links.append(link[0].strip())
            _links.append(link[0].strip())
        print('Total = {}'.format(len(_links)))
        format_strings = ','.join(['?'] * len(links))

        if len(total_links) > 0:
            sql = " UPDATE " + 'ingredients' + " set status = 1 WHERE url IN (%s)" % format_strings
            cursor.execute(sql, tuple(_links))
            connection.commit()
            print('Affected UPDATED ROWS Rows:- {0}'.format(cursor.rowcount))
    except Exception as ex:
        print('Exception in get_links')
        crash_date = time.strftime("%Y-%m-%d %H:%m:%S")
        crash_string = "".join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
        exception_string = '[' + crash_date + '] - ' + crash_string + '\n'
        print(exception_string)
    finally:
        cursor.close()
        return _links


def parse(url):
    records = []
    ingredient = ''
    c = [1, 3, 5, 6]
    sleep(random.choice(c))
    try:
        headers = {
            'authority': 'www.drugs.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,ur;q=0.8,zh-CN;q=0.7,zh;q=0.6',
            'cache-control': 'no-cache',
            # Requests sorts cookies= alphabetically
            'dnt': '1',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        print('Processing...', url, '\n')
        r = requests.get(url, headers=headers)
        print(r.status_code)
        if r.status_code != 200:
            return []

        html = r.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        ingredient_section = soup.select('h1')
        if ingredient_section:
            ingredient = ingredient_section[0].text

        ingredient = ingredient_section[0].text.strip()
        paras = soup.findAll('p')
        for para in paras:
            para_text = para.text.strip()
            if 'Brand' in para_text:
                para_split = para_text.split(':')
                if len(para_split) < 3:
                    drug_name = ''
                else:
                    drug_name = para_split[2]

                brands = para_split[1].replace('Drug class', '').split(',')
                for brand in brands:
                    records.append(
                        {
                            'ingredient': ingredient,
                            'brand': brand,
                            'ingredient_url': url,
                            'drug_name': drug_name,
                        }
                    )

        # Store data
        store_brand_products(records, connection)
    except Exception as ex:
        print('Exception in parse for the url:- ', url)
        crash_date = time.strftime("%Y-%m-%d %H:%m:%S")
        crash_string = "".join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
        exception_string = '[' + crash_date + '] - ' + crash_string + '\n'
        print(exception_string)


if __name__ == '__main__':
    connection = get_connection()
    url = 'https://www.drugs.com//ingredient/abacavir.html'

    while True:
        links = get_links(20)
        if len(links) == 0:
            break
        print(links)
        # parse(url, connection)
        with Pool(2) as p:
            result = p.map(parse, links)

        print('Round ends')
        sleep(2)
