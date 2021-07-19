FROM python:3.7.5-slim-stretch

WORKDIR /app

RUN mkdir storage && \
    mkdir storage/log && \
    touch storage/log/app.log

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]

