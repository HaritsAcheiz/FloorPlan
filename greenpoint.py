import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class GPScraper:
    base_url : str

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }

        with httpx.Client(verify=False) as client:
            response = client.get(headers=headers, url=url, follow_redirects=True)
        return response.text

    def get_img_link(self, html):
        tree = HTMLParser(html)
        items = list()
        stage1 = tree.css('html > body > section')
        for i, sub in enumerate(stage1):
            if (i > 0):
                try:
                    img_url = sub.css_first('div > div > div > img').attributes['src']
                    items.append(img_url)
                except Exception as e:
                    pass
            else:
                continue
        return items

    def get_ac_link(self, html):
        tree = HTMLParser(html)
        ac_links = list()
        stage1 = tree.css('div.flex.flex-wrap > a')
        for sub in stage1:
            try:
                ac_link = self.base_url + sub.attributes['href']
                ac_links.append(ac_link)
            except Exception as e:
                continue
        return ac_links

    def download_img(self, items):
        for item in items:
            if not os.path.exists('greenpoint'):
                os.mkdir('greenpoint')
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"greenpoint/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://greenpoint.com'
    url = 'https://greenpoint.com/interior-layouts'
    s = GPScraper(base_url=base_url)
    ac_links = []
    htmls = []
    ac_html = s.fetch(url)
    ac_links = s.get_ac_link(ac_html)
    for url in ac_links:
        print(url)
        htmls.append(s.fetch(url))
    for html in htmls:
        items = s.get_img_link(html)
        s.download_img(items)
