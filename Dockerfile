FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]