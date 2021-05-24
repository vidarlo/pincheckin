FROM alpine

LABEL pincheckin Vidar Løkken <vl@bitsex.net>

RUN apk --update add python3 py3-pip tzdata unixodbc
RUN apk add --virtual .build-deps py3-pip gcc g++ make python3-dev  libffi-dev rust openssl-dev cargo

COPY . /app
#COPY database.db /data

RUN pip3 install -r /app/requirements.txt
RUN apk del .build-deps

#VOLUME /data
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["server.py"]