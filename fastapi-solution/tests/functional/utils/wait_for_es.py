import logging

from elasticsearch import Elasticsearch
from settings import config

from utils.backoff import backoff
from utils.exceptions import RetryExceptionError

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler(filename="/var/log/waiters/es.log")
fh.setFormatter(formatter)
logger.addHandler(fh)


@backoff(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
def check_es_ready():
    es = Elasticsearch(['http://{0}:{1}/'.format(config.es_host, config.es_port)])
    if not es.ping():
        raise RetryExceptionError("Elasticsearch is not ready")


if __name__ == "__main__":
    check_es_ready()
