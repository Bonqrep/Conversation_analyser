FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /main_app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]