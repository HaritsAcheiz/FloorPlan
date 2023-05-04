import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os
import json

@dataclass
class EPScraper:
    base_url : str

    def fetch_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url)
        return response.text

    def parse_url(self, html):
        urls = []
        tree = HTMLParser(html)
        json_data = json.loads(tree.css_first('script#__NEXT_DATA__').text())
        # json_formatted_str = json.dumps(json_data, indent=2)
        i=0
        while 1:
            try:
                url = json_data['props']['initialProps']['pageProps']['Contents'][2]['data']['items'][i]['url']
                i+=1
                if url != None:
                    urls.append(self.base_url + url)
            except:
                break
        return urls

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url, follow_redirects=True)
        return response.text

    def get_img_link(self, htmls):
        items = []
        item = None
        for html in htmls:
            tree = HTMLParser(html)
            parent = tree.css_first('html > body > div > main > div.container > section')
            try:
                sub = parent.css('div.specification-tab-content__images__items > img')
                for i in sub:
                    item = i.attributes['src']
                    items.append(item)
            except:
                continue
        return items

    def download_img(self, items):
        if not os.path.exists('tagaviation'):
            os.mkdir('tagaviation')
        for item in items:
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"tagaviation/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            else:
                continue
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.tagaviation.com'
    s = EPScraper(base_url=base_url)
    parent_html = s.fetch_url('https://www.tagaviation.com/en/charter/the-fleet')
    urls = s.parse_url(parent_html)
    htmls = []
    for url in urls:
        htmls.append(s.fetch(url))
    items = s.get_img_link(htmls)
    s.download_img(items)