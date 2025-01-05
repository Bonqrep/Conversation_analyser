FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /main_app
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    && pip install --no-cache-dir --upgrade pip \
    && -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY .flaskenv .flaskenv
COPY conversation_analyser.py conversation_analyser.py
COPY config.py config.py
COPY app app

EXPOSE 8000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]