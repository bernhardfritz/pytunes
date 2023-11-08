from .database import SessionLocal
from redis import Redis
from rq import Queue
from passlib.apache import HtpasswdFile
from functools import lru_cache


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_queue():
    return Queue(connection=Redis(host="redis"))


def get_store():
    return Redis(host="redis", decode_responses=True)


@lru_cache
def get_ht():
    return HtpasswdFile("/pytunes/.htpasswd")
