FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV UWSGI_INI /webapp/uwsgi.ini
ENV STATIC_PATH /webapp/app/static

WORKDIR /webapp

ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD . .
