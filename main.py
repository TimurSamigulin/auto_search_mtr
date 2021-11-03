import json
import requests
import time
import pandas as pd

from pathlib import Path

from scripts.parsers.sites_text_parser import SitesText


def get_article_text(urls: list):
    sites = SitesText()

    file_path = Path('.', 'data', 'urls_text.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        for index, url in enumerate(urls):
            f.write(f'{index} - {url}\n')
            f.write(json.dumps(sites.get_article_text(url.strip()), ensure_ascii=False))
            f.write('\n')


if __name__ == '__main__':
    sites = SitesText()




