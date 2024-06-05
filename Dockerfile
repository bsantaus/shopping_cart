FROM python:3.10

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000
CMD fastapi run main.py