FROM python:3.7

RUN pip install pipenv

COPY /Pipfile /Pipfile
COPY /Pipfile.lock /Pipfile.lock

RUN pipenv install --system

COPY /testapp /testapp

WORKDIR /testapp
