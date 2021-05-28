#!/usr/bin/env bash

cd /ms105_exchange_engine/ || exit 1
python3 manage.py migrate
python3 manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8084 --access-log /var/log/ms105_exchange_engine/daphne_access.log exchange_engine.asgi:application
