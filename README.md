# Egglings

## What is this?

[Rustlings](https://github.com/rust-lang/rustlings) is a program with interactive exercises for Rust that teaches by example. Each exercise is run and once the
error is cleared the program is allowed to advance to the next exercise. This is
an attempt to make a similar program for Python.

## How does it run?

Within a docker container, the program loops and watches the `exercises/` folder
for changes. When you make the necessary changes for the exercise to pass, you'll
see that the exercise has passed. At this point, remove the `I AM NOT DONE` comment
from the exercise, and the program will move on to the next exercise.

## How do I get started?

First, run `make docker` to make the docker image.  Then run `make egglings` to run the image with the exercises folder mounted inside the container.

In the `exercises/` folder, there is a series of python scripts that the container
will attempt to run, and when it fails on one it will stop and show you the traceback
of what happened. Modify the file to make the script run.

Every time you save modify a file in the exercises, the container will detect it and attempt to run the latest failing test.

## Requirements

Install Docker and make sure the daemon is running, by running `docker --version`

Then, run `make docker` to make the docker image, and `make egglings` to run the exercises.

## Docker-less running

To run this on your machine, create a virtual environment for python, using python3. I suggest using [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/), but use whatever is best for you.

Then install the dependencies in the requirements file with pip:

```
pip install -r requirements.txt
```

Then run the main.py program with python:

```
python3 main.py
```

Using Docker is just a bit more convenient, since you don't have to make a virtual environment to get this running and users new to Python may not have virtual environment wrappers set up on their machine. Docker is a relatively straightforward install.
