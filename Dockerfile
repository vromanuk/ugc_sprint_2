FROM python:3.9

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

ADD . /opt/app
WORKDIR /opt/app
RUN poetry install --no-root

RUN useradd -ms /bin/bash web && chown -R web /var/log && chown -R web /var/tmp && chown -R web /opt/app
USER web

CMD python3 start.py
