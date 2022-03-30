FROM python:3.8-slim-buster

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip setuptools \
&& pip install -e .

ENTRYPOINT [ "python", "/app/src/main.py" ]
