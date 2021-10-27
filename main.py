from scripts.parsers.google_search import GoogleSearch
from scripts.parsers.sites_text_parser import SitesText

if __name__ == '__main__':
    google = GoogleSearch()
    sites = SitesText()

    urls = google.get_urls('Кабель')
    texts = []
    for url in urls:
        texts.append(sites.get_page_text(url))

    print(texts[-1:])

