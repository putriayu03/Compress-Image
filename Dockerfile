FROM python:latest
LABEL authors="Gabriel Cesar Hutagalung"

RUN pip install Flask
RUN apt update
RUN apt upgrade -y
RUN apt install -y ffmpeg

COPY . .

EXPOSE 5000

CMD  flask --app app run --host=0.0.0.0