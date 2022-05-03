from time import sleep

from elasticsearch import Elasticsearch

from settings import config


def check_es_ready():
    es = Elasticsearch(['http://{0}:{1}/'.format(config.es_host, config.es_port)])
    while not es.ping():
        sleep(1)


if __name__ == '__main__':
    check_es_ready()
