FROM tiangolo/uvicorn-gunicorn:python3.11

WORKDIR /app

COPY ./requirements.txt /backend/requirements.txt
COPY ./tests/test_requirements.txt /backend/tests/test_requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/tests/test_requirements.txt

COPY app app/

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 app.main:app