FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

EXPOSE 8000

COPY wait-for-db.sh /wait-for-db.sh
ENTRYPOINT ["/wait-for-db.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

