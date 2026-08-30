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

## Observability

The `api` service is auto-instrumented with OpenTelemetry (`opentelemetry-instrument`)
and exports traces, metrics, and logs over OTLP gRPC to the `otel-collector` service,
which prints all three signals to its own console output via a `debug` exporter.

View the exported telemetry:

```shell
docker compose logs -f otel-collector
```

Generate telemetry with a request that succeeds and one that fails:

```shell
curl -X POST http://localhost:8000/api/employees \
	-H "Content-Type: application/json" \
	-d '{"name":"John Doe","email":"john.doe@example.com","position":"Software Engineer"}'

curl -X POST http://localhost:8000/api/employees \
	-H "Content-Type: application/json" \
	-d '{"name":"John Doe","email":"invalid","position":"Software Engineer"}'
```

The collector logs should show trace spans and metric data points for both
requests, and an error log record for the failing one, all tagged with
`service.name=employee-api`.

