FROM python:3.8
EXPOSE 5052
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python","app_starter.py","server"]
