FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]