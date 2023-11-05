from .database import SessionLocal
from redis import Redis
from rq import Queue


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_queue():
    yield Queue(connection=Redis(host="redis"))


def get_store():
    yield Redis(host="redis", decode_responses=True)
