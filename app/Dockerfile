###########
# BUILDER #
###########

# pull official base image
FROM alpine:latest as build

WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add py3-pip build-base python3-dev gcc musl-dev cargo zlib-dev libxml2-dev libxslt-dev libc-dev libffi-dev openssl-dev libgcc jpeg-dev postgresql-dev \
    && pip3 install --upgrade pip \
    && pip3 install virtualenv poetry==1.0.0

RUN virtualenv venv
COPY ./poetry.lock ./pyproject.toml /src/
RUN source venv/bin/activate && poetry install --no-dev --no-root

COPY ./find_deps.sh ./find_deps.sh
RUN chmod +x ./find_deps.sh \
    && ./find_deps.sh ./venv/ > deps.txt


#########
# FINAL #
#########

# pull official base image
FROM alpine:latest

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S django -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
RUN mkdir $APP_HOME/venv
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME
COPY --from=build /src/deps.txt .
COPY --from=build /src/venv/ /src/venv/

RUN apk update \
    && apk add python3

RUN cat deps.txt \
    && cat deps.txt | xargs apk add

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME



# chown all the files to the app user
RUN chown -R django:app $APP_HOME

# change to the app user
USER django

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]