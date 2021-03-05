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
```bash
sudo apt install make
pip install --upgrade pip
pip install -r requirements.txt
./manage.py migrate
./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
./manage.py runserver
```

Все необходимые файлы вы можете найти здесь: https://gitlab.informatics.ru/2020-2021/mytischi/s105/exchange_engine/-/wikis/%D0%9D%D0%B5%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B8%D0%BC%D1%8B%D0%B5+%D1%84%D0%B0%D0%B9%D0%BB%D1%8B
