import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

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
        stage1 = tree.css('tbody > tr')
        for sub in stage1:
            url = sub.css_first('td:nth-child(2) > a').attributes['href']
            urls.append(url)
        return urls

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url)
        return response.text

    def get_img_link(self, htmls):
        items = []
        item = {'img_url':None, 'filename':None}
        for html in htmls:
            tree = HTMLParser(html)
            try:
                item['img_url'] = tree.css_first('img[style*="object-fit:contain"]').attributes['src']
                item['filename'] = tree.css_first('img[style*="object-fit:contain"]').attributes['alt']
            except:
                item['img_url'] = None
                item['filename'] = None
            items.append(item.copy())
        return items

    def download_img(self, items):
        if not os.path.exists('europair'):
            os.mkdir('europair')
        for item in items:
            if item['img_url'] != None:
                with httpx.Client() as client:
                    response = client.get(item['img_url'])
                with open(f"europair/{item['filename']}", 'wb') as f:
                    f.write(response.content)
            else:
                continue
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.europair.com'
    s = EPScraper(base_url=base_url)
    parent_html = s.fetch_url('https://www.europair.com/en/private-jet-guide')
    urls = s.parse_url(parent_html)
    htmls = []
    for url in urls:
        htmls.append(s.fetch(url))
    items = s.get_img_link(htmls)
    s.download_img(items)