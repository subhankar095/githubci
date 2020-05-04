FROM python:3

RUN mkdir -p /serving_app

RUN apt-get update -y

WORKDIR /serving_app

RUN pip3 install mysql-connector-python

RUN pip3 install flask

COPY flask_app.py /serving_app

EXPOSE 5000

CMD ["python3", "flask_app.py"]

