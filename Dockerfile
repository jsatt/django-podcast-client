FROM python:2.7

RUN adduser --quiet --gecos --disable-password app

RUN mkdir /srv/app /downloads /data \
    && chown -R app:app /srv/app /downloads /data
WORKDIR /srv/app

RUN apt-get update \
    && apt-get -y install \
        python-dev \
    && rm -rf /var/lib/apt/lists/*

COPY docker/base_app/requirements.txt ./
RUN pip install -r requirements.txt \
    && rm -rf ~/.cache

COPY --chown=app:app docker/base_app ./
COPY --chown=app:app podcast_client ./podcast_client/

USER app

RUN python manage.py syncdb --noinput \
    && python manage.py collectstatic --noinput

VOLUME /downloads /data

CMD gunicorn base_app.wsgi -w 2 -b 0.0.0.0:8000
