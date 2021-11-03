import time
import pandas as pd

from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver

from scripts.parsers.google_search import GoogleSearch
from scripts.parsers.ya_search import YaSearch


def write_urls_in_file(urls, file_path):
    """
    Сохранить urls в файл
    :param urls:
    :param file_path:
    :return:
    """
    with open(file_path, 'w') as f:
        for url in urls:
            f.write(url + '\n')


def get_urls(q: str) -> list:
    """
    Получить urls по переданному поисковому запросу
    :param q:
    :return:
    """
    google = GoogleSearch()
    yandex = YaSearch()
    urls_google = google.get_urls(q)
    urls_yandex = yandex.get_urls(q)

    urls = urls_google + urls_yandex

    del yandex
    del google
    return urls


def is_shop(url: str) -> bool:
    """
    Проверяем магазин или нет этот сайт
    :param url:
    :return:
    """
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('-headless')

    driver = webdriver.Firefox(options=firefox_options)

    driver.get(url)
    time.sleep(3)

    html_doc = BeautifulSoup(driver.page_source, features='html.parser')
    head = html_doc.find('head')
    shop_word = ('интернет магазин', 'продажа', 'каталог', 'доставка', 'интеренет-магазин', 'интернет магазине',
                 'интернет-магазине', 'яндекс.маркет', 'купить')
    head = str(head).lower()

    for word in shop_word:
        if word in head:
            return True

    driver.quit()
    driver.close()

    return False


def get_all_urls(query):
    urls_list = []
    for index, q in enumerate(query):
        time.sleep(5)
        print(f'{index}/{len(query)} - {q}')
        urls = get_urls(q)
        urls_path = Path('.', 'data', f'{q}.txt')
        write_urls_in_file(urls, urls_path)
        for url in urls:
            url_info = {}
            url_info['url'] = url
            url_info['query'] = q
            urls_list.append(url_info)

    query_path = Path('.', 'data', 'model', 'all_urls.csv')
    df_url = pd.DataFrame(urls_list)
    df_url.to_csv(query_path)


def get_model_query(columns, query_path):
    df = pd.read_csv(query_path, header=None, index_col=None, sep=';')
    df.columns = columns
    query = df['query'].unique()
    return query

if __name__ == '__main__':
    columns = ['cat1', 'cat2', 'cat3', 'query']
    query_path = Path('.', 'data', 'model', 'query.csv')

    query = get_model_query(columns, query_path)
    get_all_urls(query)
