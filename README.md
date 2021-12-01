# auto_search

Чтобы работал Selenium необходимо Добавить исполняемый 
файл драйвера firefox в PATH или перенести его в папку /usr/local/bin

https://github.com/mozilla/geckodriver/releases

Установить зависимости: pip install -r requirements.txt

- parsing 

Парсинг ссылок с Яндекс и Гугл по определенным поисковым запросам.
Все данные спаршены уже и хранятся по пути data/model/uritexts, нет 
смысла снова парсить их снова. Но чтобы запустить данный модуль, 
необходимо запустить файл main.py в корневой папке проекта.

- processing

Модуль извлечение информации из текстов, для его работы запустите 
файл scripts/processing/main_processing.py

- Файлы

Результаты выполнения модуля processing хранятся в data/result

В папке data/model/uritext хранятся все собранные тексты и ссылки на источники

В файле data/model/all_urls.csv хранятся все собранные ссылки на источники

В файле data/model/model.csv хранится семантическая модель в виде
таблицы

В файле data/model/query.csv хранятся поисковые запросы

