from utils import *
import string
import requests
from bs4 import BeautifulSoup
from time import sleep


def fetch(alpha='a', n=1):
    records = []
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
    alphabet = alpha
    url = 'https://www.drugs.com/ingredient-{}{}.html'.format(alpha, n)
    print('ORIGINAL URL = ', url)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('.contentBox ul > li > a')

        for link in links:
            if 'ingredient' in link['href'] and len(link.text.strip()) > 1:
                if 'Next' not in link.text.strip():
                    records.append(
                        {'url': link['href'].strip(),
                         'text': link.text.strip(),
                         'original_url': url
                         })
    return records


if __name__ == '__main__':
    connection = get_connection()
    alphabet_string = list(string.ascii_lowercase)
    # result = fetch()
    # for rec in result:
    #     store_ingredient_links('https://www.drugs.com/' + rec['url'], rec['text'], rec['original_url'], connection)

    for alpha in alphabet_string:
        for n in range(1, 5):
            result = fetch(alpha, n)
            for rec in result:
                store_ingredient_links('https://www.drugs.com/' + rec['url'], rec['text'], rec['original_url'], connection)

            sleep(1)
