FROM python:3.11-alpine
EXPOSE 80
RUN apk add --no-cache postgresql-dev gcc musl-dev ffmpeg
WORKDIR /pytunes
COPY ./requirements.txt /pytunes/requirements.txt
COPY ./requirements-dev.txt /pytunes/requirements-dev.txt
RUN pip install --no-cache-dir --upgrade -r /pytunes/requirements-dev.txt
COPY ./src /pytunes/src
COPY ./start.sh /pytunes/
COPY ./.htpasswd /pytunes/
RUN chmod +x ./start.sh
CMD ./start.sh