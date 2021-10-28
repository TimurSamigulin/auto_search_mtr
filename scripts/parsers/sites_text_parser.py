import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


class SitesText:
    """
    Класс для получения текста из переданного url
    """

    def get_page_text(self, link):
        try:
            simple_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
            response = requests.get(link, headers=simple_headers, timeout=(5, 5))
        except (HTTPError, ConnectionError, Timeout, RequestException, OSError) as e:
            print(e)
        else:
            if response.status_code == 200:
                if 'text/html' in response.headers.get('Content-Type'):
                    html_doc = BeautifulSoup(response.text, features='html.parser')

                    if main_tag := html_doc.find('html'):
                        normalized_text = SitesText.normalize_page_text(main_tag.getText())
                        content = f'Page link: {link}\n\n{normalized_text}'
                        return content

    @staticmethod
    def normalize_page_text(text):
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n ', '\n', text)
        return text


if __name__ == '__main__':
    x = SitesText().get_page_text('https://www.elec.ru/publications/analitika-rynka/6591/')
    print(x.split('\n'))