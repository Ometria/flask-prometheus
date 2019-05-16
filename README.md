# flask-prometheus
Flask Middleware for Prometheus Metrics

## Usage

```python
from flask_prometheus import Prometheus

Prometheus(app)
```

## Metrics
```python
REQUESTS = Counter(
    "http_request_total", "Total Requests", labelnames=["method", "path", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "Total Requests",
    labelnames=["method", "path", "status"],
)
SIZE = Summary(
    "http_response_size_bytes",
    "Response Sizes",
    labelnames=["method", "path", "status"],
)
```
