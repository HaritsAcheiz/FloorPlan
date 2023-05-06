import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class APScraper:
    base_url : str

    def generate_url(self):
        urls = []
        for page in range(1,4):
            if page == 1:
                urls.append(f"https://www.skyservicesjet.com/en/jets_flotte/")
            else:
                urls.append(f"https://www.skyservicesjet.com/en/jets_flotte/page/{page}/")
        return urls

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
        stage1 = tree.css('div.owl-carousel.owl-airpartner.owl-airpartner--image-gallery > div > img')
        for sub in stage1:
            try:
                img_url = self.base_url + sub.attributes['data-src']
                items.append(img_url)
            except Exception as e:
                pass
        return items

    def get_ac_link(self, html):
        tree = HTMLParser(html)
        ac_links = list()
        stage1 = tree.css('a.aircraft-item__link.btn.btn-blue.btn-min-width-220')
        for sub in stage1:
            try:
                ac_link = self.base_url + sub.attributes['href']
                ac_links.append(ac_link)
            except Exception as e:
                continue
        return ac_links

    def download_img(self, items):
        for item in items:
            if not os.path.exists('airpartner'):
                os.mkdir('airpartner')
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"airpartner/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.airpartner.com'
    s = APScraper(base_url=base_url)
    ac_links = []
    htmls = []
    ac_html = (s.fetch('https://www.airpartner.com/en/aircraft-guide/private-jets/'))
    ac_links.extend(s.get_ac_link(ac_html))
    for url in ac_links:
        htmls.append(s.fetch(url))
    print(htmls[0])
    for html in htmls:
        items = s.get_img_link(html)
        print(items)
        s.download_img(items)
