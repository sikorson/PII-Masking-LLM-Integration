FROM python:3.12.0

WORKDIR /app

COPY ./app /app
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python -m spacy download en_core_web_sm

