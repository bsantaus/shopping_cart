FROM python:3.10

RUN mkdir /app
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD fastapi run main.py