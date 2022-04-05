FROM python:3.8.10

ADD . .

COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "uvicorn", "main:app", "--reload","--host", "0.0.0.0" ]

