FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY ./vaquita .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 22229

ENV DATABASE_URL=""

CMD ["python", "server.py"]
