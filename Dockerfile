FROM python:3.9.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry --disable-pip-version-check

COPY ./ ./app
WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-root
RUN chmod +x /app/src/entrypoint.py

# Uncomment this line if deploying to Github Actions..
CMD [ "python3", "/app/src/entrypoint.py" ]