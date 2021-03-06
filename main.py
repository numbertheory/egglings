import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import yaml
import subprocess
import os
from subprocess import PIPE, Popen

SKIP_CHECKS = []


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_exercise_order():
    with open("exercises/exercises.yaml") as f:
        exercises = yaml.safe_load(f)
    return exercises


def flake_check(exercise, flake8_check=True):
    flake8_cmd = "flake8 exercises/{exercise}.py".format(
        exercise=exercise)
    if flake8_check:
        exit_code = subprocess.call(
            flake8_cmd, shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        if exit_code != 0:
            p = Popen(["flake8",
                       "exercises/{exercise}.py".format(
                        exercise=exercise)],
                      stdin=PIPE,
                      stdout=PIPE)
            output, err = p.communicate()
            return output.decode("utf-8")


def check_exercises(flake8_check=False):
    for exercise in exercises:
        if exercise not in SKIP_CHECKS:
            cmd = "python3 exercises/{exercise}.py".format(
                exercise=exercise)

            try:
                flake_check(exercise, flake8_check)
                exit_code = subprocess.call(cmd,
                                            shell=True,
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.STDOUT)
                if exit_code != 0:
                    print(
                        "❌ exercises/{exercise}.py failed".format(
                            exercise=exercise)
                         )
                    return subprocess.check_output(cmd, shell=True)
                else:
                    print(
                        "✅ exercises/{exercise}.py passed".format(
                            exercise=exercise)
                         )
                    SKIP_CHECKS.append(exercise)
            except subprocess.CalledProcessError:
                break


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
        if os.getenv('EGGLINGS_FLAKE8'):
            clear_screen()
            check_exercises(flake8_check=True)
        else:
            clear_screen()
            check_exercises(flake8_check=False)


if __name__ == "__main__":
    exercises = load_exercise_order().get('exercises', [])
    event_handler = ModificationWatcher()
    observer = Observer()
    observer.schedule(event_handler, path='exercises/', recursive=False)
    observer.start()

    try:
        if os.getenv('EGGLINGS_FLAKE8'):
            exercise_check = check_exercises(flake8_check=True)
        else:
            exercise_check = check_exercises(flake8_check=False)
        if exercise_check:
            print(exercise_check)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        exit(0)
    observer.join()
