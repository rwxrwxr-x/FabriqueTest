FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y \
    bash        \
    postgresql  \
    libffi-dev \
    python3-dev

ENV APP_DIR /src/backend

RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}
ADD ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . .
RUN chmod -R ugo+x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]