FROM python:3.9

ENV HOME=/code

RUN apt-get update -y && apt-get upgrade -y 
RUN pip install --upgrade pip
RUN addgroup web && adduser web --home $HOME --ingroup web
RUN mkdir /var/log/waiters/ && chown -R web:web /var/log/waiters

WORKDIR $HOME

COPY ./fastapi-solution/requirements.txt .
RUN pip install -r requirements.txt

COPY ./fastapi-solution/src/ .

USER web
ENTRYPOINT ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
