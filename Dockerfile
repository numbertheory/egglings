FROM python:3.7-alpine3.12

WORKDIR /app

COPY main.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
