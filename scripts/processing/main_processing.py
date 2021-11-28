from pathlib import Path
from scripts.processing import processing

"""
    Вызов функций из processing с передачей входных и выходных файлов
"""

def get_en_org_info():
    input_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/texts.csv'
    output_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/en_org_info.csv'
    processing.get_en_orgs_info(input_file, output_file)


def get_ru_org_info():
    input_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/texts.csv'
    output_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/ru_org_info1.csv'
    processing.get_ru_orgs_info(input_file, output_file)


def get_gost():
    output_file = '../../data/model/uritexts/Кабель определение/kabel_gost.txt'
    processing.get_gost_info(output_file)


def get_kabel_class():
    output_file = '../../data/model/uritexts/Классификация кабелей/kabel_class.txt'
    processing.get_kabel_class(output_file)

def get_share_prices():
    output_dir = Path('..', '..', 'data', 'model', 'uritexts', 'Прогноз цены на силовой кабель')
    processing.get_share_prices(output_dir)

if __name__ == '__main__':
    # get_en_org_info()
    get_ru_org_info()
    # get_gost()
    # get_kabel_class()
    # get_share_prices()