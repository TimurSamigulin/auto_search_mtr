import pandas as pd
from scripts.processing.organization_processing import OrgProcessing
from scripts.processing.gost_processing import KabelInfo


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
    for org in en_orgs:
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
    for org in ru_orgs:
        org_info = org_proc.get_ru_org_info(org)
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
    kabel_class = gost_proc.get_kabel_class('Кабели силовые')

    with open(output_file, 'w', encoding='utf-8') as fw:
        [fw.write(kabel) for kabel in kabel_class]

    return kabel_class


