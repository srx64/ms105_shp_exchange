# Exchange Engine
Кратко: эмулятор биржи

Развёрнуто: 
- Акции
- Покупка / Продажа
- Торговля в лонг
- Торговля в шорт
- Торговля с плечом
- Margin call
- История - загружается в виде массива котировок. Позже - эмулируется ботами.

## Технологический стек:
- Python 3
- Django 3
- Django REST Framework

## Quickstart
В главной папке проекта необходимо создать папку `media`, в которой нужно создать папку `avatars`. После этого 
следует перейти по ссылке и сохранить в папку `avatars` файл `preset.jpg`.

Также в главной папке проекта необходимо создать папку `data` и поместить туда .csv файлы из Wiki проекта.
```bash
sudo apt install make
pip install --upgrade pip
pip install -r requirements.txt
sudo apt-get install postgresql
sudo systemctl start postgresql.service
sudo systemctl enable postgresql.service
sudo -u postgres psql
create database exchange;
create user shp with encrypted password 'promprog';
grant all privileges on database exchange to shp;
\q
sudo -u postgres psql exchange < exchange.sql
./manage.py migrate
./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
python price_bot.py
./manage.py runserver
```

Все необходимые файлы вы можете найти здесь: https://gitlab.informatics.ru/2020-2021/mytischi/s105/exchange_engine/-/wikis/%D0%9D%D0%B5%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B8%D0%BC%D1%8B%D0%B5+%D1%84%D0%B0%D0%B9%D0%BB%D1%8B
