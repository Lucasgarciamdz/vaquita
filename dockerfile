# syntax=docker/dockerfile:1.2

# Stage 1: Build
FROM python:3.9-slim-buster AS build

WORKDIR /app

# Leverage Docker layer caching by copying and installing requirements first
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Stage 2: Run
FROM python:3.9-slim-buster AS run

WORKDIR /app

# Copy from build stage
COPY --from=build /app .

# Run the application
CMD ["python", "your_app.py"]