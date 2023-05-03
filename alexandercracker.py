import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class ACScraper:
    base_url : str

    def generate_url(self):
        urls = []
        aircrafts = ['acj-320', 'bbj-737-max']
        configs = [
            {'a': 'vip-layout', 'b': 'vip-cabin-interior-layouts'},
            {'a': 'head-of-state-layout', 'b': 'head-of-state-interior-cabin-layouts'},
            {'a': 'corporate-layout', 'b': 'corporate-interior-layouts'},
            {'a': 'multi-role-transport-layout', 'b': 'multi-role-transport'}
        ]
        for aircraft in aircrafts:
            for config in configs:
                urls.append(f"https://www.alexandercraker.com/aircraft-interior-architecture/{config['a']}/{aircraft}-{config['b']}")
        return urls

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
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
        items = list()
        stage1 = tree.css('div.columns-29.w-row > div')
        for sub in stage1:
            stage2 = sub.css('div.mask-10.w-slider-mask > div')
            for item in stage2:
                try:
                    img_url = item.css_first('img').attributes['src']
                except:
                    img_url = None
                items.append(img_url)
        return items

    def download_img(self, items):
        for item in items:
            if not os.path.exists('alexandercracker'):
                os.mkdir('alexandercracker')
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"alexandercracker/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.alexandercraker.com'
    s = ACScraper(base_url=base_url)
    urls = s.generate_url()
    htmls = []
    for url in urls:
        htmls.append(s.fetch(url))
    # htmls = s.fetch('https://www.alexandercraker.com/aircraft-interior-architecture/vip-layout/acj-320-vip-cabin-interior-layouts')
    for html in htmls:
        items = s.get_img_link(html)
        s.download_img(items)
