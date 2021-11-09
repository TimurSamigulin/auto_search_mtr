from scripts.processing import processing

def get_en_org_info():
    input_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/texts.csv'
    output_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/en_org_info.csv'
    processing.get_en_orgs_info(input_file, output_file)

def get_ru_org_info():
    input_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/texts.csv'
    output_file = '../../data/model/uritexts/Крупнейшие мировые производители силового кабеля/ru_org_info.csv'
    processing.get_ru_orgs_info(input_file, output_file)