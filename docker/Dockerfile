FROM ubuntu:latest
MAINTAINER Daria Mishkina <dasha.mishkina117@gmail.com>

ADD ./ /ms105_exchange_engine
WORKDIR /ms105_exchange_engine/
RUN apt-get update && apt-get install -y build-essential nano python3 python3-dev python3-pip supervisor libpq-dev
RUN pip install --no-cache-dir -r ./requirements.txt

RUN mkdir -p /var/log/ms105_exchange_engine
RUN chmod u+x /var/log/ms105_exchange_engine

RUN mkdir -p /var/log/supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD exec /usr/bin/supervisord --nodaemon
