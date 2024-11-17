FROM python:3.11.10-alpine3.20

# Đặt thư mục làm việc là /app
WORKDIR /app

# Sao chép tất cả các tệp 
COPY . .

# Cài đặt các gói thông tin cần thiết
RUN pip install -r requirements.txt

# Mở cổng 5555
EXPOSE 5555

# Đặt entrypoint để chạy API
ENTRYPOINT ["python", "main.py", "--host=0.0.0.0", "--port=5555", "--reload=True", \
    "--workers=4", "--log_level=info", "--limit_max_request=1000", "--limit_concurrency=1000", "--backlog=5000"]
# ENTRYPOINT ["python", "main.py", "--host=0.0.0.0", "--port=5555", "--reload=True", "--workers=4", \
#     "--log_level=info", "--limit_max_request=1000", "--limit_concurrency=1000", "--backlog=5000", \
#     "--ssl_keyfile=/etc/nginx/ssl/private.pem", "--ssl_certfile=/etc/nginx/ssl/cert.pem"]