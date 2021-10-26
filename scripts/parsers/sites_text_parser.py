from bs4 import BeautifulSoup
import re
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

class SitesParser:

    def get_page_text(self, link):
        try:
            simple_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
            response = requests.get(link, headers=simple_headers, timeout=(5, 5))
        except (HTTPError, ConnectionError, Timeout, RequestException, OSError) as e:
            print(e)
        else:
            if response.status_code == 200:
                # print(response.headers.get('Content-Type'))
                if 'text/html' in response.headers.get('Content-Type'):
                    html_doc = BeautifulSoup(response.text, features='html.parser')

                    if main_tag := html_doc.find('html'):
                        normalized_text = self.normalize_page_text(main_tag.getText())
                        content = f'Page link: {link}\n\n{normalized_text}'
                        return content

    def normalize_page_text(self, text):
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n ', '\n', text)
        return text

if __name__ == '__main__':
    x = SitesParser().get_page_text('https://www.elec.ru/publications/analitika-rynka/6591/')
    print(x.split('\n'))