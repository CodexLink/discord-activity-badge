
LABEL name="Discord Rich Presence Activity Badge Container"
LABEL version="beta.0.11282020"
LABEL description="A containerized python application that aims to display User's Discord Rich Presence to their Github Profile Badge."
LABEL maintainer="Janrey 'CodexLink' Licas <self.codexlink@gmail.com>"

FROM python:3.8.6-slim-buster

RUN pip install pipenv
RUN pipenv install
RUN pipenv shell

WORKDIR /src
RUN chmod +x entrypoint.py

ENTRYPOINT ["entrypoint.py"]
# CMD ["main.py"]
