import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta



class ModificationWatcher(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = datetime.now()

    def on_modified(self, event):
        # On Linux and inside the container, it will double report file changes
        # so this prevents that from happening.
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
        print(f'Event type: {event.event_type}  path : {event.src_path}')


if __name__ == "__main__":
    event_handler = ModificationWatcher()
    observer = Observer()
    observer.schedule(event_handler, path='exercises/', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        exit(0)
    observer.join()
