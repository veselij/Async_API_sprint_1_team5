#!/bin/sh

echo "starting tests"
python -m utils.wait_for_es && python -m utils.wait_for_redis && python -m pytest src/
echo "tests finished"


exec "$@"
