import logging
from selenium import webdriver
from bs4 import BeautifulSoup

from scripts.parsers.search import Search


class YaSearch(Search):
    """
    Класс для парсинга Яндекс запросов. пришлось использовать Selenium и имитировать работу браузера, так как
    Яндекс активно борится с парсигом своих сервисов.
    """

    def __init__(self):
        self._firefox_options = webdriver.FirefoxOptions()
        self._firefox_options.add_argument('-headless')

        self._driver = webdriver.Firefox(options=self._firefox_options)

    def get_urls(self, q: str, start: int = 0):
        """
        Метод возвращает список url из Яндекс запроса
        :param q: Запрос
               start: номер начальной страницы, начинается с 0
        :return: Список собранных url
        """
        base_url = 'https://yandex.ru/search/?text={}&p={}'.format(q, start)

        try:
            self._driver.get(base_url)
        except OSError:
            logger.exception(f'OSError: {base_url}')
            return []

        soup = BeautifulSoup(self._driver.page_source, 'lxml')
        with_quest = []

        titles = soup.findAll('h2', 'OrganicTitle')
        for title in titles:
            link = title.find('a').get('href')
            with_quest.append(link)

        return with_quest

    def __del__(self):
        self._driver.quit()



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    ya = YaSearch()
    urls = ya.get_urls('Кабель')
    print(len(urls))
    for url in urls:
        print(url)

if __name__ == '__ya_search__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)