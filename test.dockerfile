FROM python:3

COPY requirements.txt /app/

RUN python -m pip install -r /app/requirements.txt

COPY src /app/

WORKDIR /app

CMD ["python", "run.py", "test"]
