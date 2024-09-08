FROM python:3.9-slim

RUN pip install --no-cache-dir \
    pymongo \
    psycopg2-binary \
    sqlalchemy \
    redis \
    pandas \
    numpy

RUN mkdir /app

RUN mkdir -p /mnt/azure-site-packages

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]