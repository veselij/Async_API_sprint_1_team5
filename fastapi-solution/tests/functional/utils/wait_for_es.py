import os
import sys
from time import sleep

from elasticsearch import Elasticsearch

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from settings import ConfigSettings


def check_es_ready():
    config = ConfigSettings()
    es = Elasticsearch(['http://{0}:{1}/'.format(config.es_host, config.es_port)])
    while not es.ping():
        sleep(1)


if __name__ == '__main__':
    check_es_ready()
