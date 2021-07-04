FROM python:3.9.6-slim-buster

LABEL name="Discord Rich Presence Activity Badge Container"
LABEL version="dev.4.07042021"
LABEL description="To be done later."
LABEL maintainer="Janrey 'CodexLink' Licas <self.codexlink@gmail.com>"

RUN ls
RUN pip install poetry
WORKDIR /../src
RUN poetry install
# RUN poetry shell

RUN chmod +x entrypoint.py

ENTRYPOINT ["entrypoint.py"]