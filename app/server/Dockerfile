FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 8888

COPY ./main /app

WORKDIR /app/main

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]