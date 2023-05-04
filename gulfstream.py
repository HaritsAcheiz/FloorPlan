import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class GSScraper:
    base_url : str

    def parse_url(self, html):
        urls = []
        tree = HTMLParser(html)
        stage1 = tree.css('ul#menu-aircraft > li')
        for sub in stage1:
            url = self.base_url + sub.css_first('a').attributes['href']
            urls.append(url)
        return urls

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url)
        if response.status_code == 200:
            return response.text

    def fetch_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url)
        if response.status_code == 200:
            return response.text

    def get_img_link(self, htmls):
        items = []
        item = None
        for html in htmls:
            if html != None:
                tree = HTMLParser(html)
                try:
                    stage1 = tree.css('div.carousel.desktop-section.cabinConfig-slider > div')
                    for sub in stage1:
                        item = self.base_url + sub.css_first('img').attributes['src']
                        items.append(item)
                except:
                    continue
            else:
                continue
        return items

    def download_img(self, items):
        if not os.path.exists('gulfstream'):
            os.mkdir('gulfstream')
        for item in items:
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"gulfstream/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            else:
                continue
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.gulfstream.com'
    s = GSScraper(base_url=base_url)
    parent_html = s.fetch_url('https://www.gulfstream.com/en/aircraft/')
    urls = s.parse_url(parent_html)
    htmls = []
    for url in urls:
        htmls.append(s.fetch(url))
    items = s.get_img_link(htmls)
    s.download_img(items)