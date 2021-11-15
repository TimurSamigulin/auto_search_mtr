import time
import logging
import pandas as pd

from multiprocessing import Pool
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver

from scripts.parsers.google_search import GoogleSearch
from scripts.parsers.ya_search import YaSearch
from scripts.util.driver import Driver


class SiteSearch():

    def write_urls_in_file(self, urls: list, file_path: Path):
        """
        Сохранить urls в файл
        :param urls: список ссылок
        :param file_path: путь до файла куда сохранить список ссылок
        :return:
        """
        with open(file_path, 'w') as f:
            for url in urls:
                f.write(url + '\n')

    def get_urls(self, q: str) -> list:
        """
        Получить urls по переданному поисковому запросу используя Гугл и Яндекс поисковики
        :param q: поисковой запрос
        :return: список уникальных собранных ссылок
        """
        google = GoogleSearch()
        yandex = YaSearch()
        urls_google = google.get_urls(q)
        urls_yandex = yandex.get_urls(q)

        urls = urls_google + urls_yandex

        del yandex
        del google
        return list(set(urls))

    def is_shop(self, url) -> bool:
        """
        Проверяем магазин или нет этот сайт. Используется selenium, чтобы максимально имитировать работу браузера и
        получить доступ ко всем сайтам. Так некоторые из ссылок используют переадресацию и обычным get запросом не полу-
        чить информацию со страницы. А так же некоторые сайты борятся с парсингом и получить другими способами информацию
        с них затруднительно.
        :param url: ссылка на сайт
        :return: True если это интернет магазин
        """
        # print(url)
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('-headless')

        driver = webdriver.Firefox(options=firefox_options)
        try:
            driver.get(url)
        except Exception as e:
            print(f'except {e}')
            return True

        html_doc = BeautifulSoup(driver.page_source, features='html.parser')
        head = html_doc.find('head')
        shop_word = ('интернет магазин', 'продажа', 'каталог', 'доставка', 'интеренет-магазин', 'интернет магазине',
                     'интернет-магазине', 'яндекс.маркет', 'купить')
        head = str(head).lower()

        for word in shop_word:
            if word in head:
                driver.quit()
                return True

        driver.quit()
        return False

    def all_urls(self, query: list, data_path: Path):
        """
        Спарсить ссылки по списку переданных запросов
        :param query: список запросов для которых нужно получить источники
        :param data_path: путь до папки data куда будут сохраться источники в файлы под название query.txt
        :return: список словарей формата [{'url': url, 'query': query}, ..., {}]
        """
        urls_list = []

        for index, q in enumerate(query):
            print(f'{index + 1}/{len(query)} - {q}')
            time.sleep(5)

            urls = self.get_urls(q)
            urls_path = data_path / f'{q}.txt'  # Путь до папки data

            for url in urls:
                url_info = {}
                url_info['url'] = url
                url_info['query'] = q
                urls_list.append(url_info)

            self.write_urls_in_file(urls, urls_path)

        return urls_list

    def get_model_query(self, query_path, columns, query_column='query', header=None, index_col=None, sep=';'):
        """Получить список запросов из файла где сохранены запросы"""
        df = pd.read_csv(query_path, header=header, index_col=index_col, sep=sep)
        df.columns = columns
        query = df[query_column].unique()
        return query

    def get_all_urls(self, columns: list, query_path: Path, data_path: Path):
        """
        Получить список всех ссылок по переданным запросам и сохранение их в файлы
        :param columns: список названий колонок для query DataFrame,
        :param query_path: путь до csv файла где сохранен query DataFrame
        :param data_path: путь до папки Data
        :return: список ссылок
        """
        query = self.get_model_query(query_path, columns)

        urls_list = self.all_urls(query, data_path)

        df_url = pd.DataFrame(urls_list)
        query_path = Path('.', 'data', 'model', 'all_urls.csv')
        df_url.to_csv(query_path)

        return urls_list

    def check_shop_url(self, urls: list, thread=5) -> list:
        """
        Проверяем список ссылок являются они магазином или нет
        :param urls: список ссылок
        thread: количество потоков
        :return: список из Булевых значений где True - магазин, False - не магазин
        """
        count_proc = thread
        pool = Pool(processes=count_proc)
        all_shops = pool.map(self.is_shop, urls)
        return all_shops


if __name__ == '__main__':
    search = SiteSearch()
    search.get_urls('Рынок кабельной продукции')

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
