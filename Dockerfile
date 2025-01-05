FROM python:3.11.11-alpine

# Đặt thư mục làm việc là /app
WORKDIR /app

# Sao chép tất cả các tệp 
COPY . .

# Cài đặt các gói thông tin cần thiết
RUN pip install -r requirements.txt

# Mở cổng 5555
EXPOSE 5001

# Đặt entrypoint để chạy API
ENTRYPOINT ["python", "main.py", "--host=0.0.0.0", "--port=5001", "--reload=False", \
    "--workers=4", "--log_level=info", "--limit_max_request=1000", "--limit_concurrency=1000", "--backlog=5000"]