from timeit import default_timer

from flask import request
from prometheus_client import Counter, Histogram, Summary


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

# excludes paths generated by connexion lib as well as /metrics and /healthz
METRICS_EXCLUDE_ENDPOINTS = (
    "._swagger_ui_static",
    "._swagger_ui_index",
    "._swagger_json",
    "static",
    ".api_metrics",
    ".api_healthz",
)


def initialise_metrics(app):
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in METRICS_EXCLUDE_ENDPOINTS:
            for method in rule.methods:
                if method in (
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                ):  # to avoid timeseries for "HEAD" and "OPTIONS" that are added by connexion
                    for status in ("2xx", "3xx", "4xx", "5xx"):
                        REQUESTS.labels(method, rule.rule, status)
                        LATENCY.labels(method, rule.rule, status)
                        SIZE.labels(method, rule.rule, status)


def before_request():
    request.start_time = default_timer()


def after_request(resp):
    if request.url_rule and request.url_rule.endpoint not in METRICS_EXCLUDE_ENDPOINTS:
        path = request.url_rule.rule if request.url_rule else "-"
        duration = max(default_timer() - request.start_time, 0)
        status_code = f"{resp.status[0]}xx"
        LATENCY.labels(request.method, path, status_code).observe(duration)
        REQUESTS.labels(request.method, path, status_code).inc()
        if "content-length" in resp.headers:
            size = int(resp.headers["content-length"])
            SIZE.labels(request.method, path, status_code).observe(size)
    return resp


class Prometheus:
    def __init__(self, app):
        self.app = app
        self.init_app(app)

    def init_app(self, app):
        initialise_metrics(app)
        app.before_request(before_request)
        app.after_request(after_request)
