FROM python:3.9

ENV HOME=/code

RUN apt-get update -y && apt-get upgrade -y 
RUN pip install --upgrade pip
RUN addgroup web && adduser web --home $HOME --ingroup web

WORKDIR $HOME

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/ .

USER web
