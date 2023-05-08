import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os
import re

@dataclass
class CJScraper:
    base_url : str

    def generate_url(self):
        urls = []
        for page in range(1,208):
                urls.append(f"https://centraljets.com/plane/{page}")
        return urls

    def fetch(self, url):
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }
        try:
            with httpx.Client() as client:
                response = client.get(headers=headers, url=url, follow_redirects=True)
            result = response.text
        except Exception as e:
            print(e)
            result = None
        return result

    def get_img_link(self, html):
        tree = HTMLParser(html)
        items = list()
        stage1 = tree.css('div#layout > img')
        for sub in stage1:
            try:
                img_url = self.base_url + sub.attributes['href']
                items.append(img_url)
            except Exception as e:
                pass
        return items

    def get_ac_link(self, html):
        tree = HTMLParser(html)
        ac_links = list()
        stage1 = tree.css('div.wrapper')
        for sub in stage1:
            try:
                ac_link = self.base_url + re.sub(r"\s+", "", sub.css_first('a').attributes['href'])
                ac_links.append(ac_link)
            except Exception as e:
                continue
        return ac_links

    def download_img(self, items):
        for item in items:
            try:
                if not os.path.exists('centraljets2'):
                    os.mkdir('centraljets2')
                if item != None:
                    with httpx.Client() as client:
                        response = client.get(item)
                    with open(f"centraljets2/{item.split('/')[-1]}", 'wb') as f:
                        f.write(response.content)
                print('Image downloaded successfully!')
            except:
                print('Image download failed!')
                continue

if __name__ == '__main__':
    base_url = 'https://centraljets.com'
    s = CJScraper(base_url=base_url)
    urls = s.generate_url()
    ac_htmls = []
    ac_links = []
    htmls = []
    for url in urls:
        ac_htmls.append(s.fetch(url))
    for html in ac_htmls:
        ac_links.extend(s.get_ac_link(html))
    for url in ac_links:
        htmls.append(s.fetch(url))
    for html in htmls:
        items = s.get_img_link(html)
        s.download_img(items)
