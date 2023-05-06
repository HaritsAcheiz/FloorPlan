import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os
import re

@dataclass
class SJScraper:
    base_url : str

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url, follow_redirects=True)
        return response.text

    def get_img_link(self, html):
        tree = HTMLParser(html)
        items = list()
        stage1 = tree.css('div.c-charter-gallery__slide')
        for sub in stage1:
            try:
                s = sub.attributes['style']
                img_url = re.search('\(([^)]+)', s).group(1)
                items.append(img_url)
            except Exception as e:
                pass
        return items

    def download_img(self, items):
        for item in items:
            if not os.path.exists('freestream'):
                os.mkdir('freestream')
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"freestream/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.freestream.com'
    s = SJScraper(base_url=base_url)
    html = s.fetch('https://www.freestream.com/charter/')
    items = s.get_img_link(html)
    s.download_img(items)
