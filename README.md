# auto_search

Чтобы работал Selenium необходимо Добавить исполняемый файл драйвера firefox в PATH или перенести его в папку /usr/local/bin

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

Результаты модуля processing хранятся в data/result