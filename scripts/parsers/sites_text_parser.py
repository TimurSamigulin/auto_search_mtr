import re
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


class SitesText:
    """
    Класс для получения текста из переданного url
    """

    def get_page_text(self, link):
        """
        Парсим текст с сайта
        :param link:
        :return: весь текст с сайта
        """
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

    def get_article_text(self, url) -> dict:
        '''
        С помощью библиотеки Article, достаем основной контент с новостных сайтов
        :param url: ссылка на текст
        :return: словарь с инфой
        '''
        article = Article(url)
        article.download()
        article.parse()
        information = {}
        information['date'] = article.publish_date
        information['text'] = article.text
        information['top_image'] = article.top_image
        article.nlp()
        information['keywords'] = article.keywords
        information['summary'] = article.summary
        return information

    @staticmethod
    def normalize_page_text(text):
        """
        Убираем лишние пробелы
        :param text:
        :return:
        """
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n ', '\n', text)
        return text


if __name__ == '__main__':
    x = SitesText().get_page_text('https://www.elec.ru/publications/analitika-rynka/6591/')
    print(x.split('\n'))
