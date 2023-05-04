import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os

@dataclass
class ACScraper:
    base_url : str

    def generate_url(self):
        urls = []
        types = ['very-light-jets', 'light-jets', 'super-light-jets', 'mid-size-jets', 'super-mid-size-jets', 'heavy-jets', 'ultra-long-range-jets', 'vip-airliners', 'turbo-props']
        for type in types:
            urls.append(f"{self.base_url}/{type}")
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
        stage1 = tree.css('div.fusion-fullwidth.fullwidth-box.fusion-builder-row-2.fusion-flex-container.fleet.nonhundred-percent-fullwidth.non-hundred-percent-height-scrolling > div > div')
        # '/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[12]/div/div/div/div/div[1]/ul/li[1]/div/div/a/img'
        for i, sub in enumerate(stage1):
            try:
                img_url = sub.css_first('ul.fusion-carousel-holder > li:nth-of-type(3) > div > div > a').attributes['href']
                items.append(img_url)
            except Exception as e:
                continue
        return items

    def download_img(self, items):
        for item in items:
            if not os.path.exists('pristinejet'):
                os.mkdir('pristinejet')
            if item != None:
                with httpx.Client() as client:
                    response = client.get(item)
                with open(f"pristinejet/{item.split('/')[-1]}", 'wb') as f:
                    f.write(response.content)
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://pristinejet.com/en'
    s = ACScraper(base_url=base_url)
    urls = s.generate_url()
    htmls = []
    for url in urls:
        htmls.append(s.fetch(url))
    for html in htmls:
        items = s.get_img_link(html)
        s.download_img(items)
