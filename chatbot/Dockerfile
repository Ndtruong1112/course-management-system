FROM python:3.11-slim

WORKDIR /app

# Cài đặt curl để kiểm tra kết nối nếu cần
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python dependencies
COPY chatbot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn chatbot
COPY chatbot/ ./chatbot/

EXPOSE 7860

ENV PYTHONUNBUFFERED=1
ENV BACKEND_URL=http://backend:8080

CMD ["python", "chatbot/web_app.py"]
