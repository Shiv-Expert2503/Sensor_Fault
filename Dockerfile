FROM python:3.11.6

WORKDIR /app

COPY . /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
