FROM python:3

COPY requirements.txt /app/

RUN python -m pip install -r /app/requirements.txt

COPY src /app/

WORKDIR /app

ARG GITHUB_HANDLE=invalid_username
ENV GITHUB_HANDLE ${GITHUB_HANDLE}

ARG GITHUB_TOKEN=invalid_token
ENV GITHUB_TOKEN ${GITHUB_TOKEN}

ARG NUM_TASKS=10
ENV NUM_TASKS ${NUM_TASKS}

CMD python run.py --handle $GITHUB_HANDLE --token $GITHUB_TOKEN --tasks $NUM_TASKS
