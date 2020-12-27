import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import yaml
import subprocess

def load_exercise_order():
    with open("exercises/exercises.yaml") as f:
        exercises = yaml.safe_load(f)
    return exercises

def check_exercises():
    for exercise in exercises:
        cmd = "python3 exercises/{exercise}.py".format(exercise=exercise)
        try:
            exit_code = subprocess.call(cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
            if exit_code != 0:
                return subprocess.check_output(cmd, shell=True)
        except:
            pass

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
    exercises = load_exercise_order().get('exercises', [])
    event_handler = ModificationWatcher()
    observer = Observer()
    observer.schedule(event_handler, path='exercises/', recursive=False)
    observer.start()

    try:
        exercise_check = check_exercises()
        if exercise_check:
            print(exercise_check)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        exit(0)
    observer.join()
