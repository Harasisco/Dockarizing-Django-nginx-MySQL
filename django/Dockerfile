FROM python:3.10
WORKDIR /code

ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt  
RUN pip install --no-cache-dir -r requirements.txt

COPY wait_for_db.py wait_for_db.py

COPY . .
