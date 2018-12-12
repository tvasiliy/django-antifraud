FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /django-antifraud
WORKDIR /django-antifraud
COPY requirements.txt /django-antifraud/
RUN pip install -r requirements.txt
COPY . /django-antifraud/
