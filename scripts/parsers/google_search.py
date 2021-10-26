import re
import requests
import logging
from bs4 import BeautifulSoup


class GoogleSearch:

    def _get_site(self, q: str, start: int = 0) -> list:
        '''
            Метод возвращает списков url с гугл запроса

            Parameters:
            q -- Гугл запрос
            start -- Номер начального сайта

        '''

        base_url = 'https://www.google.com/search?q={}&start={}'.format(
            q, start)

        try:
            responce = requests.get(base_url)
        except OSError:
            logger.exception(f'OSError: {base_url}')

        soup = BeautifulSoup(responce.text, 'lxml')

        with_quest = []

        # Ищем нужные url и очищаем их
        for link in soup.find_all('a'):
            if link.get('href').startswith(
                    '/url') and 'google.com' not in link.get('href'):
                link = link.get('href')[7:]
                link = link[:re.search('&sa=', link).span()[0]]
                with_quest.append(link)

        return with_quest

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    google = GoogleSearch()._get_site(q='Кабель')
    print(google)