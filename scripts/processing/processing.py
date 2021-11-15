import time
import pandas as pd
from scripts.processing.organization_processing import OrgProcessing
from scripts.processing.gost_processing import KabelInfo
from scripts.processing.prices_processing import PricesInfo

"""
    Файл с функциями вызовами всех функций которые отвечают за извлечение информации
"""


def get_en_org_from_text(input_file):
    """
    Получаем список предполагаемых иностранных компаний из текстов
    :return:
    """
    org_proc = OrgProcessing()
    df = pd.read_csv(input_file,
                     index_col=0)

    orgs = org_proc.get_ner_tag(df.text.values)
    en_orgs = org_proc.normalize_en_tag(orgs)

    return en_orgs


def get_en_orgs_info(input_file, output_file):
    """
    Парсим адрес данной организации
    :return:
    """
    org_proc = OrgProcessing()
    en_orgs = get_en_org_from_text(input_file)
    en_org_info = []
    for i, org in enumerate(en_orgs):
        time.sleep(1)
        print(f'en {i}/{len(en_orgs)}')
        org_info = org_proc.get_en_org_info(org)
        if org_info:
            en_org_info.append(org_info)

    result = pd.DataFrame(en_org_info)
    result.to_csv(output_file)
    return en_org_info


def get_ru_org_from_text(input_file):
    """Получаем список русских компаний из текста"""
    org_proc = OrgProcessing()
    df = pd.read_csv(input_file,
                     index_col=0)

    orgs = org_proc.get_ner_tag(df.text.values)
    ru_orgs = org_proc.normalize_rus_tag(orgs)

    return ru_orgs


def get_ru_orgs_info(input_file, output_file):
    """
    Парсим инфу о русских компаниях
    :return:
    """
    org_proc = OrgProcessing()
    ru_orgs = get_ru_org_from_text(input_file)
    ru_org_info = []
    for i, org in enumerate(ru_orgs):
        print(f'ru {i}/{len(ru_orgs)}')
        org_info = org_proc.get_ru_org_info(org)
        if org_info:
            ru_org_info.append(org_info)

    result = pd.DataFrame(ru_org_info)
    result.to_csv(output_file)
    return ru_org_info


def get_gost_info(output_file):
    gost_proc = KabelInfo()
    gost = gost_proc.get_gost_info()
    with open(output_file, 'w', encoding='utf-8') as fw:
        fw.write(gost)

    return gost


def get_kabel_class(output_file):
    gost_proc = KabelInfo()
    kabel_class = gost_proc.get_kabel_class(q='Кабели силовые')

    with open(output_file, 'w', encoding='utf-8') as fw:
        fw.write(','.join(kabel_class))

    return kabel_class


def get_share_prices(output_dir):
    """
    Функция парсит выбранные котировки и записывает их в файлы в переданную директорию
    :param output_dir:
    :return:
    """
    price_info = PricesInfo()
    share_prices = ['copper', 'USDRUB', 'aluminum']
    for share_price in share_prices:
        print(share_price)
        prices_info = price_info.parse_share_price(share_price)
        prices_info.to_csv(output_dir / f'{share_price}.csv')
        mean_price = price_info.mean_price(prices_info)
        mean_price.to_csv(output_dir / f'{share_price}_year_mean.csv')
        mean_price = price_info.mean_price_month(prices_info)
        mean_price.to_csv(output_dir / f'{share_price}_month_mean.csv')
        base_price = price_info.base_price(prices_info.close.values[-1], share_price)
        if base_price:
            with open(output_dir / f'{share_price}_base_price.txt', 'w') as fw:
                fw.write(str(base_price))
