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

