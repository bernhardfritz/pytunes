#!/bin/sh
mkdir -p /data/.pytunes
python -m src.database
rq worker -u redis://redis:6379 &
python -m src.sync &
uvicorn src.main:app --host 0.0.0.0 --port 80