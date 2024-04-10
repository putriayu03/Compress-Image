FROM python:latest
LABEL authors="Gabriel Cesar Hutagalung"

RUN pip install Flask


COPY . .

EXPOSE 5000

CMD  flask --app Api run --host=0.0.0.0