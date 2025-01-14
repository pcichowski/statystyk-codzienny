# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]
