import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from pathlib import Path
from scripts.parsers.google_search import GoogleSearch
from scripts.parsers.ya_search import YaSearch
from scripts.parsers.sites_text_parser import SitesText


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
    return urls


def get_article_text(urls: list):
    sites = SitesText()

    file_path = Path('.', 'data', 'urls_text.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        for index, url in enumerate(urls):
            f.write(f'{index} - {url}\n')
            f.write(json.dumps(sites.get_article_text(url.strip()), ensure_ascii=False))
            f.write('\n')


def is_shop(url: str) -> bool:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('-headless')

    driver = webdriver.Firefox(options=firefox_options)

    driver.get(url)

    html_doc = BeautifulSoup(driver.page_source, features='html.parser')
    head = html_doc.find('head')
    shop_word = ('интернет магазин', 'продажа', 'каталог', 'доставка', 'интеренет-магазин', 'интернет магазине',
                 'интернет-магазине', 'яндекс.маркет', 'купить')
    head = str(head).lower()
    # print(head)
    for word in shop_word:
        if word in head:
            return True

    return False


if __name__ == '__main__':
    sites = SitesText()
    file_path = Path('.', 'data', 'urls.txt')

    with open(file_path, 'r') as f:
        urls = f.readlines()

    # for url in urls:
    for url in urls:
        print(url)
        print(is_shop(url))



