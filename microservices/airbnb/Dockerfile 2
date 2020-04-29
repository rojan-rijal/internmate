FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt && apt-get install -y curl
COPY ./app /app
