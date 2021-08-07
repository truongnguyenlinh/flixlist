FROM python:3.9.5-slim-buster

RUN mkdir /flixlist
COPY requirements.txt /flixlist
WORKDIR /flixlist
RUN pip3 install -r requirements.txt

COPY . /flixlist

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]