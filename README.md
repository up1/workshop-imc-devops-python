# Workshop with Python
* Python 3.14
* FastAPI
* Developer Testing with Pytest
* API testing with Postman
* MySQL Connector/Python

## Run

```shell
docker compose up --build
```

Create an employee at `http://localhost:8000/api/employees`:

```shell
curl -X POST http://localhost:8000/api/employees \
	-H "Content-Type: application/json" \
	-d '{"name":"John Doe","email":"john.doe@example.com","position":"Software Engineer"}'
```

## Test

```shell
cd api
pytest
```

The API tests replace the repository dependency with a mock, so they cover the
controller and service without requiring a running MySQL instance.
