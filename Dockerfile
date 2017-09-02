FROM tiangolo/uwsgi-nginx-flask:python2.7

MAINTAINER Andrew Sosa <andrew@acmatfsu.org>

ENV UWSGI_INI /webapp/uwsgi.ini
ENV STATIC_PATH /webapp/app/static

ADD . /webapp
WORKDIR /webapp

RUN pip install -r requirements.txt
