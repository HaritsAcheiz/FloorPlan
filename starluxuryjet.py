import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class SLScraper:
    base_url : str

    def generate_url(self):
        html = self.fetch(self.base_url)
        tree = HTMLParser(html)
        stage1 = tree.css('li#menu-item-1846 > ul > li')
        urls = []
        for sub in stage1:
            urls.append(sub.css_first('a').attributes['href'])
        return urls

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }
        print(url)
        with httpx.Client() as client:
            response = client.get(headers=headers, url=url, follow_redirects=True)
        print(response)
        return response.text

    def get_img_link(self, html):
        tree = HTMLParser(html)
        items = list()
        try:
            img_url = tree.css_first('html > body > div:nth-of-type(1) > div > div > article > section:nth-of-type(3) > div:nth-of-type(2) > div > div > div > div:nth-of-type(2) > figure >div > img').attributes['data-src']
            items.append(img_url)
        except Exception as e:
            img_url = None
            items.append(img_url)
        return items

    def get_ac_link(self, html):
        tree = HTMLParser(html)
        ac_links = list()
        stage1 = tree.css('a.vc_gitem-link.vc-zone-link')
        for sub in stage1:
            try:
                ac_link = sub.attributes['href']
                ac_links.append(ac_link)
            except Exception as e:
                continue
        return ac_links

    def download_img(self, items):
        for item in items:
            if not os.path.exists('starrluxuryjets'):
                os.mkdir('starrluxuryjets')
            if item != None:
                print(item)
                try:
                    with httpx.Client() as client:
                        response = client.get(item)
                    with open(f"starrluxuryjets/{item.split('/')[-1].split('?')[0]}", 'wb') as f:
                        f.write(response.content)
                    print('Image downloaded successfully!')
                except:
                    print('Image download failed!')

if __name__ == '__main__':
    base_url = 'https://starrluxuryjets.com'
    s = SLScraper(base_url=base_url)
    urls = s.generate_url()
    ac_htmls = []
    ac_links = []
    htmls = []
    for url in urls[1:]:
        ac_htmls.append(s.fetch(url))
    print('ac_html_ok')
    for html in ac_htmls:
        ac_links.extend(s.get_ac_link(html))
    print('ac_link_ok')
    for url in ac_links:
        htmls.append(s.fetch(url))
    print('html_ok')
    for html in htmls:
        items = s.get_img_link(html)
        s.download_img(items)
