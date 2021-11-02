from pathlib import Path
from scripts.parsers.google_search import GoogleSearch
from scripts.parsers.ya_search import YaSearch
from scripts.parsers.sites_text_parser import SitesText

def write_urls_in_file(urls, file_path):
    with open(file_path, 'w') as f:
        for url in urls:
            f.write(url + '\n')

def get_urls(q: str) -> list:
    google = GoogleSearch()
    yandex = YaSearch()
    urls_google = google.get_urls(q)
    urls_yandex = yandex.get_urls(q)

    urls = urls_google + urls_yandex
    return urls

if __name__ == '__main__':
    sites = SitesText()

    file_path = Path('.', 'data', 'urls.txt')

    with open(file_path, 'r') as f:
        urls = f.readlines()

    for index, url in enumerate(urls):
        print(index)
        print(url)
        print(sites.get_article_text(url.strip()))



