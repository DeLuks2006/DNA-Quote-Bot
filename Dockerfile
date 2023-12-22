FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk add inotify-tools

COPY ./entrypoint.sh ./

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["./entrypoint.sh"]
