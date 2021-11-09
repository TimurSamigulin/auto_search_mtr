import requests
import logging

from bs4 import BeautifulSoup
from scripts.util.driver import Driver

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

class PricesInfo():

    def parse_share_price(self, product):
        base_url = f'https://www.profinance.ru/chart/?s={product}&hist=true'

        driver = Driver(headless=True).get_driver()

        driver.get(base_url)

        input = driver.find_elements_by_class_name('combobutton')
        input[-1].click()
        driver.find_element_by_id('tt_table').find_elements_by_tag_name('tr')[-1].click()
        input[-2].click()
        driver.find_element_by_id('pt_table').find_elements_by_tag_name('tr')[-1].click()
        table = driver.find_element_by_id('table_history').find_elements_by_tag_name('tr')

        prices_info = []
        for tr in table[1:-1]:
            td = tr.find_elements_by_tag_name('td')
            prices_info.append({'close': td[0].text, 'date': td[1].text.split('.')[-1]})

        driver.quit()

        return prices_info


if __name__ == '__main__':
    prices = PricesInfo()
    print(prices.parse_share_price('copper'))