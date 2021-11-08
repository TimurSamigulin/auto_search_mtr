import json
import requests
import pandas as pd

from pathlib import Path

from scripts.parsers.sites_text_parser import SitesText
from scripts.parsers.parse_urls import SiteSearch



def get_article_text(urls: list):
    sites = SitesText()

    file_path = Path('.', 'data', 'urls_text.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        for index, url in enumerate(urls):
            f.write(f'{index} - {url}\n')
            f.write(json.dumps(sites.get_article_text(url.strip()), ensure_ascii=False))
            f.write('\n')

def get_texts(input_path, output_path, drop_shop=True):
    sites = SitesText()
    df = pd.read_csv(input_path, index_col=None, header=0)
    articles = []
    query = df['query'].values
    is_shop = df['is_shop'].values

    for index, url in enumerate(df.url.values):
        print(url)
        if drop_shop:
            if is_shop[index]:
                continue
        article = sites.get_article_text(url)
        if not article['text']:
            article['text'] = sites.get_page_text(url)

        article['url'] = url
        article['query'] = query[index]
        article['is_shop'] = is_shop[index]
        articles.append(article)

    df = pd.DataFrame(articles)
    df.to_csv(output_path)
    return articles

def get_article_urls(all_urls_path, output_path):
    """
    Пробегается по всем спаршеным ссылкам, распределяет их по категориям и проверяет магазины это или нет
    :param all_urls_path: файл со всеми ссылками
    :param output_path: паппка в которой будут создаваться подпапки с инфой по разделу
    :return:
    """
    shop_search = SiteSearch()

    df = pd.read_csv(all_urls_path, header=0)
    df.drop(df.iloc[:, :1], axis=1, inplace=True)
    queries = df['query'].unique()
    for query in queries:
        print(query)
        df1 = df[df['query'] == query]
        urls = df1.url.values

        all_shops = shop_search.check_shop_url(urls)

        df1['is_shop'] = pd.Series(all_shops, index=df1.index)
        output_path_dir = output_path / query
        if output_path_dir.is_dir():
            output_path_dir.mkdir()
        df1.to_csv(output_path_dir / 'urls.csv', index=None)

if __name__ == '__main__':
    sites = SitesText()

    directories = Path('data', 'model', 'uritexts').glob('*')
    for directory in directories:
        input_path = directory / 'urls.csv'
        output_path = directory / 'texts.csv'
        get_texts(input_path, output_path)

    # all_urls_path = Path('data', 'model', 'all_urls.csv')
    # output_path = Path('data', 'model', 'uritexts')
    # get_article_urls(all_urls_path, output_path)

    # columns = ['cat1', 'cat2', 'cat3', 'query']
    # query_path = Path('data', 'model', 'query.csv')
    # data_path = Path('data')

    # site_search = SiteSearch()
    # site_search.get_all_urls(columns, query_path, data_path)




