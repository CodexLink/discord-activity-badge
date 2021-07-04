FROM python:3.9.6-slim-buster

LABEL name="Discord Rich Presence Activity Badge Container"
LABEL version="dev.4.07042021"
LABEL description="To be done later."
LABEL maintainer="Janrey 'CodexLink' Licas <self.codexlink@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

COPY ./ /app
WORKDIR /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-root
WORKDIR /app/src
RUN chmod +x entrypoint.py

# CMD [ "python3", "entrypoint.py" ]
CMD [ "python3", "src/entrypoint.py" ]