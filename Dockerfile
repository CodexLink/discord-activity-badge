FROM python:3.9.2-slim-buster

LABEL name="Discord Rich Presence Activity Badge Container"
LABEL version="dev.4.07042021"
LABEL description="To be done later."
LABEL maintainer="Janrey 'CodexLink' Licas <self.codexlink@gmail.com>"

RUN pip install poetry
RUN ls
RUN poetry install
# RUN poetry shell

WORKDIR /src
RUN chmod +x entrypoint.py

ENTRYPOINT ["entrypoint.py"]