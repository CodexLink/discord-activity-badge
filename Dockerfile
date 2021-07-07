FROM python:3.9.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./ ./app
WORKDIR /app
RUN chmod +x /app/src/entrypoint.py \
&& pip install poetry==1.1.7 --no-cache-dir --disable-pip-version-check \
&& poetry config virtualenvs.create false \
&& poetry install --no-dev --no-interaction --no-root

# Uncomment this line if deploying to Github Actions..
CMD [ "python3", "/app/src/entrypoint.py" ]