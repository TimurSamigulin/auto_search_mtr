import re
import logging
import time
import pandas as pd
import numpy as np
from selenium import webdriver
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

    def get_ner_tag(self, texts) -> list:
        orgs = []
        for index, text in enumerate(texts):
            print(index)
            if text is np.nan:
                print('skip')
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
        orgs_norm = [org for org in orgs if not ('\n' in org['name']) or ('\t' in org['name'])]
        orgs_norm = [org for org in orgs_norm if len(org['name']) > 5]
        en_org = []
        for i, org in enumerate(orgs_norm):
            en_len = re.findall(r"[A-Za-z]", org['name'])
            if len(en_len) > 2:
                en_org.append(org['name'])
        return list(set(en_org))

    def get_ru_org_info(self, org_name):
        base_url = 'https://www.rusprofile.ru/search-advanced'
        driver = Driver(headless=True).get_driver()
        driver.get(base_url)
        org_input = driver.find_element_by_id('advanced-search-query')
        time.sleep(3)
        org_input.send_keys(org_name)
        time.sleep(3)

        org_info = {}
        try:
            driver.find_element_by_class_name('all-count')
        except:
            print('Не найдено компании')
            return 0

        company_list = driver.find_elements_by_class_name('company-item')
        for index, company in enumerate(company_list):
            # Почему-то selenium при поиске xpath по строке ищет по всей странцие а не только по выбранной части
            org_activity = company.find_elements_by_xpath("//dt[text()[contains(.,'Основной вид деятельности')]]/../dd")

            if org_activity[index].text.find('кабел') != -1:
                org_info['org_activity'] = org_activity[index].text
                org_info['name'] = company.find_element_by_class_name('finded-text').text
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

if __name__ == '__main__':
    org_processing = OrgProcessing()
    print(org_processing.get_ru_org_info('Спецкабель'))

