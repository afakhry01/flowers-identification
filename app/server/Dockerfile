FROM python:3.9

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

COPY ./main /app

WORKDIR /app/main

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]