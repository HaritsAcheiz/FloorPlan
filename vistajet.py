import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class VJScraper:
    base_url : str

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url)
        print(response)
        return response.text

    def get_img_link(self, html):
        tree = HTMLParser(html)
        items = list()
        item = {'img_url': None, 'filename': None}
        for html in htmls:
            tree = HTMLParser(html)
            try:
                stage1 = tree.css('img[tag="general"]')
                for sub in stage1:
                    item['img_url'] = self.base_url + sub.attributes['src']
                    item['filename'] = sub.attributes['alt']
                    items.append(item.copy())
            except:
                item['img_url'] = None
                item['filename'] = None
        return items

    def get_ac_link(self, html):
        tree = HTMLParser(html)
        ac_links = list()
        stage1 = tree.css('a.uk-link-reset')
        for sub in stage1:
            try:
                ac_link = self.base_url + sub.attributes['href']
                ac_links.append(ac_link)
            except Exception as e:
                continue
        return ac_links

    def download_img(self, items):
        if not os.path.exists('vistajet'):
            os.mkdir('vistajet')
        for item in items:
            if item['img_url'] != None:
                with httpx.Client() as client:
                    response = client.get(item['img_url'])
                with open(f"vistajet/{item['filename']}.svg", 'wb') as f:
                    f.write(response.content)
            else:
                continue
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.vistajet.com'
    url = 'https://www.vistajet.com/en/private-jets/'
    s = VJScraper(base_url=base_url)
    ac_links = []
    htmls = []
    ac_html = s.fetch(url)
    ac_links = s.get_ac_link(ac_html)
    for url in ac_links:
        htmls.append(s.fetch(url))
    for html in htmls:
        items = s.get_img_link(html)
        print(items)
        s.download_img(items)
