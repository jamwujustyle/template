FROM python:3.11-alpine3.17

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN apk update \
    && apk add --no-cache --virtual .build-deps build-base postgresql-dev \
        && apk add --no-cache postgresql-libs \
        \
        && pip install --upgrade pip \
        \
        && pip install --no-cache-dir -r requirements.txt \
        \
    && apk del .build-deps \
    \
    && rm -rf /var/cache/apk/*

RUN chown -R lord:lord /app


COPY . .

RUN mkdir -p /app/media

EXPOSE 8000







