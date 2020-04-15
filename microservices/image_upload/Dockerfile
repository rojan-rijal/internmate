FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt && apt-get install -y curl
ENV CLIENT_SECRET LTIAJZ45ZXBSFKI1IVDDTPRKORPAACSAA5A2TKFZBBDT4YO0 
ENV CLIENT_ID KF45MQCPJBCBJRTL1BTN1CPK3C4SI4YDCB5NKVMZXWDZAKAJ
COPY ./app /app
