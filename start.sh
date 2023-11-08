#!/bin/sh
mkdir -p /data/.pytunes
cd src/
python -m pytunes.database
rq worker -u redis://redis:6379 &
python -m pytunes.sync &
uvicorn pytunes.main:app --host 0.0.0.0 --port 80