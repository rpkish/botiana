#################################
# Botiana Dockerfile for Alpine #
#################################
FROM python:3.7.4-alpine3.10
MAINTAINER rpkish

# Build deps
RUN apk update \
    && apk add --virtual build-dependencies build-base py3-lxml libxml2-dev libxslt-dev

# Install botiana and copy modified settings and dictionaries 
RUN mkdir /usr/local/botiana/
COPY ./botiana.py ./settings.py ./requirements.txt ./common.py ./keywords.py ./legacy_modules.py  \
     ./message_router.py ./settings.py ./slack_commands.py /usr/local/botiana/

# run configuration steps
RUN pip install -r /usr/local/botiana/requirements.txt

# Fire up botiana
ENTRYPOINT cd /usr/local/botiana && /usr/local/bin/python3 -u ./botiana.py
