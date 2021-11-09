import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class KabelInfo():

    def get_gost_info(self):
        base_url = 'https://docs.cntd.ru/document/1200011353'

        try:
            responce = requests.get(base_url)
        except OSError:
            logger.exception(f'OSError: {base_url}')
            return {}

        try:
            soup = BeautifulSoup(responce.text, 'lxml')
            named = soup.find('b', text='Кабельное изделие').parent.parent.parent
            named = named.find_all('td')[1].text
        except Exception:
            return ''

        return named

    def get_kabel_class(self, q):
        base_url = f'https://www.stroyinf.ru/cgi-bin/mck/okp.cgi?f3={q}'

        try:
            responce = requests.get(base_url)
        except OSError:
            logger.exception(f'OSError: {base_url}')
            return {}

        responce.encoding = 'utf-8'

        soup = BeautifulSoup(responce.text, 'lxml')
        li = soup.find('li', id='t3')
        kabel_class = li.findAll('b')
        kabel_class = [kabel.text[8:] for kabel in kabel_class]

        return kabel_class


if __name__ == '__main__':
    info = KabelInfo()
    info.get_kabel_class('Кабели силовые')
