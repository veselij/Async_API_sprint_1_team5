#!/bin/sh

echo "starting tests"
python utils/wait_for_es.py && python utils/wait_for_redis.py && python -m pytest src/
echo "tests finished"


exec "$@"
