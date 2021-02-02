FROM alpine

LABEL pincheckin Vidar Løkken <vl@bitsex.net>

RUN apk --update add python3

COPY . /app

RUN pip3 install -r requirements.txt


VOLUME /data
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["server.py"]