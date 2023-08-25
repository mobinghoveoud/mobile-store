FROM python:3.11

WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip
COPY requirements.txt /src/
RUN pip install -r requirements.txt

# copy project
COPY . /src/
