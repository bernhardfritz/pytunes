import glob
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from . import crud, models
from .database import engine
from .dependencies import get_db, get_queue
from .util import (
    cleanup,
    create_track,
    handle_created,
    handle_deleted,
    sha1_to_uuid,
    sha1sum,
)

JOB_TIMEOUT = 600


class Watcher:
    DIRECTORY_TO_WATCH = "/data/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except BaseException:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(PatternMatchingEventHandler):
    def __init__(self):
        super(Handler, self).__init__(ignore_directories=True, patterns=["*.mp3"])

    def on_created(self, event):
        queue = get_queue()
        queue.enqueue(handle_created, event.src_path, job_timeout=JOB_TIMEOUT)

    def on_deleted(self, event):
        handle_deleted()


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    db = next(get_db(), None)
    queue = get_queue()
    cleanup(db)
    db_ids = crud.get_track_ids(db)
    fs_ids = {}
    for file_path in glob.glob("/data/**/*.mp3", recursive=True):
        fs_ids[sha1_to_uuid(sha1sum(file_path))] = file_path
    added = [(id, file_path) for (id, file_path) in fs_ids.items() if id not in db_ids]
    for id, file_path in added:
        queue.enqueue(create_track, file_path, id, job_timeout=JOB_TIMEOUT)
    w = Watcher()
    w.run()
