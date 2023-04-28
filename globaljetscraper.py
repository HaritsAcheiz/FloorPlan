import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class GJScraper:
    base_url : str
    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            # Cookie: tarteaucitron=!googletagmanager=true; _ga_P78NTC4EP4=GS1.1.1682649984.1.1.1682651531.0.0.0; _ga=GA1.2.2003308644.1682649985; _gid=GA1.2.1431257394.1682649985
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers'
        }

        with httpx.Client() as client:
            response = client.get(headers=headers, url=url)
        return response.text

    def get_img_link(self, html):
        tree = HTMLParser(html)
        child = tree.css('html > body > div:nth-of-type(1) > div > main > div > div:nth-of-type(3) > div:nth-of-type(2) > div > div > div')
        items = list()
        for item in child:
            article = {'AC_Type': None, 'img_src1':None, 'img_src2':None}
            try:
                article['AC_Type'] = item.css_first('article > h2 > a > span').text()
                try:
                    article['img_src1'] = self.base_url + item.css_first('article > div > div.field.field--name-field-configurations.field--type-entity-reference-revisions.field--label-above > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > img').attributes['src']
                except:
                    article['img_src1'] = None
                try:
                    article['img_src2'] = self.base_url + item.css_first('article > div > div.field.field--name-field-configurations.field--type-entity-reference-revisions.field--label-above > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(2) > img').attributes['src']
                except:
                    article['img_src2'] = None
                items.append(article)
            except:
                continue
        return items

    def download_img(self, items):
        for item in items:
            if not os.path.exists('globaljet_fp'):
                os.mkdir('globaljet_fp')
            if item['img_src1'] != None:
                with httpx.Client() as client:
                    response = client.get(item['img_src1'])
                with open(f"globaljet_fp/{item['img_src1'].split('/')[-1]}.jpg", 'wb') as f:
                    f.write(response.content)
            if item['img_src2'] != None:
                with httpx.Client() as client:
                    response = client.get(item['img_src2'])
                with open(f"globaljet_fp/{item['img_src2'].split('/')[-1]}.jpg", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    s = GJScraper(base_url='https://globaljet.aero')
    for page in range(1,2):
        url = f'https://globaljet.aero/index.php/en/taxonomy/term/13?page={page}'
        html = s.fetch(url)
        items = s.get_img_link(html)
        s.download_img(items)
