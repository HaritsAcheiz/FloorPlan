import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class IBCScraper:
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
        stage1 = tree.css('img.img-responsive')
        for sub in stage1:
            try:
                img_url = sub.attributes['src']
                items.append(img_url)
            except Exception as e:
                pass
        return items

    def get_ac_link(self, html):
        tree = HTMLParser(html)
        ac_links = list()
        stage1 = tree.css('span.catItemImage')
        for sub in stage1:
            try:
                ac_link = self.base_url + sub.css_first('a').attributes['href']
                ac_links.append(ac_link)
            except Exception as e:
                continue
        return ac_links

    def download_img(self, items):
        for item in items:
            if not os.path.exists('ibc'):
                os.mkdir('ibc')
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"ibc/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.ibc-aviation.com'
    s = IBCScraper(base_url=base_url)
    ac_links = []
    htmls = []
    ac_html = (s.fetch('https://www.ibc-aviation.com/en/fleet.html'))
    ac_links = s.get_ac_link(ac_html)
    print(ac_links)
    for url in ac_links:
        htmls.append(s.fetch(url))
    for html in htmls:
        items = s.get_img_link(html)
        print(items)
        s.download_img(items)
