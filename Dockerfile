FROM python:latest
LABEL authors="Gabriel Cesar Hutagalung"

RUN pip install Flask
RUN pip install Pillow

COPY . .

EXPOSE 5000

CMD  flask --app app run --host=0.0.0.0