FROM python:3.8.6-slim-buster
# This Dockerfile is untested. Will check once in development phase.

LABEL name="Discord Rich Presence Activity Badge Container"
LABEL version="dev.1.06222021"
LABEL description="A containerized python application that aims to display User's Discord Rich Presence to their Github Profile Badge."
LABEL maintainer="Janrey 'CodexLink' Licas <self.codexlink@gmail.com>"

RUN pip install poetry
RUN poetry shell
RUN pipenv install

WORKDIR /src
RUN chmod +x entrypoint.py

ENTRYPOINT ["entrypoint.py"]
