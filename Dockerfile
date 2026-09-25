FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from api_platform import APIService; print('AI API ready')"]
