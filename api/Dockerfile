FROM python:3.14
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
RUN opentelemetry-bootstrap -a install
COPY . .

# Testing the application
RUN pytest --maxfail=1 --disable-warnings -q

CMD ["opentelemetry-instrument", "fastapi", "run", "/api/main.py", "--host", "0.0.0.0", "--port", "80"]