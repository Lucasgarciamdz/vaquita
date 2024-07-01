FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY ./vaquita .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 22229

ENV DATABASE_URL=postgresql://lucas:OnyYdjcX8nE9DlcRd98dN65DGBFsHmxn@dpg-cpst8piju9rs73ahjr80-a.oregon-postgres.render.com/vaquita_4y1j

CMD ["python", "server.py"]