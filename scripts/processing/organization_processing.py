"""
    Данный файл содержит класс для извлечения и получения информации об основных российских и иностранных
    производителях кабельной продукции.

    Функции:
    get_ner_tag -> dict, функция извлекает названия организаций из текстов
    normalize_rus_tag -> list, предобработка русских организаций
    normalize_en_tag -> dict, предобработка иностранных организаций
    get_ru_org_info -> dict, возвращет российских производителей кабельной продукции и информацию о них
    get_en_org_info -> dict, возврщает иностранных производителей кабельной продукции и их адресс
"""

import logging
import re
import time

import numpy as np
import requests
from bs4 import BeautifulSoup
from natasha import (Doc,
                     Segmenter,
                     NewsEmbedding,
                     NewsMorphTagger,
                     NewsSyntaxParser,
                     NewsNERTagger,
                     )

from scripts.util.driver import Driver

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class OrgProcessing():
    """
    Класс для получения информации об Российских и иностранных организациях
    """

    def get_ner_tag(self, texts) -> list:
        """Функция для получения NER тэгов из текста, оставляем только NER рганизаций"""
        orgs = []
        for index, text in enumerate(texts):
            if text is np.nan:
                continue
            doc = Doc(text)
            doc.segment(segmenter)
            doc.tag_morph(morph_tagger)
            doc.parse_syntax(syntax_parser)
            doc.tag_ner(ner_tagger)
            for span in doc.spans:
                if (span.type == 'ORG' or span.type == 'LOC'):
                    orgs.append({'name': span.text, 'type': span.type})

        return orgs

    def normalize_rus_tag(self, orgs: list) -> list:
        """Проводим нормализацию списка Российских организаций
        orgs: список организаций
        """
        orgs_norm = [org for org in orgs if not ('\n' in org['name']) or ('\t' in org['name'])]
        orgs_norm = [org for org in orgs_norm if len(org['name']) > 5]
        all_orgs_rus = []
        for org in orgs_norm:
            o = re.search('[\"\'«“].+[\"\'»”]', org['name'])
            if o:
                all_orgs_rus.append(o.group(0))
        all_orgs_rus = list(set(all_orgs_rus))
        all_orgs_rus = [org for org in all_orgs_rus if len(org) > 5]

        return all_orgs_rus

    def normalize_en_tag(self, orgs: list) -> list:
        """проводим нормализацию списка иностранных организаций
        orgs: список организаций
        """
        orgs_norm = [org for org in orgs if not ('\n' in org['name']) or ('\t' in org['name'])]
        orgs_norm = [org for org in orgs_norm if len(org['name']) > 5]
        en_org = []
        for i, org in enumerate(orgs_norm):
            en_len = re.findall(r"[A-Za-z]", org['name'])
            if len(en_len) > 2:
                en_org.append(org['name'])
        return list(set(en_org))

    def get_ru_org_info(self, org_name):
        """
        Полуем информацию о Российской организации
        :param org_name: название орги
        :return: словарь с информацией об организации
        """
        base_url = 'https://www.rusprofile.ru/search-advanced'
        driver = Driver(headless=True).get_driver()
        driver.get(base_url)
        time.sleep(3)
        org_input = driver.find_element_by_id('advanced-search-query')
        org_input.send_keys(org_name)
        time.sleep(3)

        org_info = {}
        try:
            driver.find_element_by_class_name('all-count')
        except:
            print('Не найдено компании')
            return 0

        company_list = driver.find_elements_by_class_name('company-item')
        if not company_list:
            return 0
        for index, company in enumerate(company_list):

            org_activity = company.find_elements_by_xpath("//dt[text()[contains(.,'Основной вид деятельности')]]/../dd")
            if org_activity:
                return 0
            if org_activity[index].text.find('кабел') != -1:
                org_info['org_activity'] = org_activity[index].text
                org_info['name'] = org_name
                org_info['address'] = company.find_element_by_class_name('company-item__text').text

                try:
                    directors = company.find_elements_by_xpath\
                        ("//dt[text()[contains(.,'Генеральный директор')]]/../dd")
                    org_info['director'] = directors[index].text
                except Exception:
                    org_info['director'] = '-'

                try:
                    main_orgs = company.find_elements_by_xpath\
                        ("//dt[text()[contains(.,'Управляющая организация')]]/../dd")
                    org_info['main_org'] = main_orgs[index].text
                except Exception:
                    org_info['main_org'] = '-'

                ogrn_list = company.find_elements_by_xpath("//dt[text()[contains(.,'ОГРН')]]/../dd")
                org_info['OGRN'] = ogrn_list[index].text

                inn_list = company.find_elements_by_xpath("//dt[text()[contains(.,'ИНН')]]/../dd")
                org_info['INN'] = inn_list[index].text

                date_list = company.find_elements_by_xpath("//dt[text()[contains(.,'Дата регистрации')]]/../dd")
                org_info['date'] = date_list[index].text
                break

        driver.quit()
        return org_info

    def get_en_org_info(self, org_name):
        """
        Информация об иностранной организации
        :param org_name: название организации
        :return: словарь с инфомацией о организации
        """
        base_url = 'https://www.google.com/search?q={}'.format(
            org_name)

        try:
            responce = requests.get(base_url)
        except OSError:
            logger.exception(f'OSError: {base_url}')
            return {}

        soup = BeautifulSoup(responce.text, 'lxml')


        address = soup.find_all('span', 'BNeawe tAd8D AP7Wnd')
        if address:
            return {'name': org_name, 'address': address[0].string}
        else:
            return {}

if __name__ == '__main__':
    org_processing = OrgProcessing()
    address = org_processing.get_en_org_info('SKET Verseilmaschinenbau GmbH')
    print(address)

