FROM ubuntu:latest

MAINTAINER Mehmet Yalcin <dryalcinmehmet@gmail.com>


###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.0-alpine as builder

# set work directory
WORKDIR /usr/src/source

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TERM xterm
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev bash nano  wget dpkg

RUN apk add --update nodejs nodejs-npm \
    && npm install -g react-tools
# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/source/
RUN echo "Flake8 is in deactive status."
#RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/source/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.0-alpine

# create directory for the source user
RUN mkdir -p /home/source

# create the source user
RUN addgroup -S source && adduser -S source -G source

# create the appropriate directories
ENV HOME=/home/source
ENV source_HOME=/home/source/web
RUN mkdir $source_HOME
RUN mkdir $source_HOME/staticfiles
RUN mkdir $source_HOME/mediafiles
WORKDIR $source_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/source/wheels /wheels
COPY --from=builder /usr/src/source/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*


# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh $source_HOME

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev bash nano  wget dpkg

RUN apk add --update nodejs nodejs-npm \
    && npm install -g react-tools


# copy project
COPY . $source_HOME
WORKDIR $source_HOME/app/templates/dash/AdminLTE/
RUN npm install
RUN npm run production
WORKDIR $source_HOME

# chown all the files to the source user
# RUN chown -R source:source $source_HOME

# change to the source user
USER source

# run entrypoint.prod.sh
ENTRYPOINT ["/home/source/web/entrypoint.prod.sh"]
