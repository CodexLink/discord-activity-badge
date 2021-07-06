FROM python:3.9.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry --disable-pip-version-check

COPY ./ /app
WORKDIR /app
RUN ls
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-root
RUN ls -a
RUN pwd
WORKDIR /app/src
RUN ls -a
RUN pwd
RUN chmod +x entrypoint.py

# CMD [ "python3", "entrypoint.py", "--running-on-local" ] # Uncomment this line if deploying / testing locally.
CMD [ "python3", "entrypoint.py" ] # Uncomment this line if deploying to Github Actions.