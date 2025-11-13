from prometheus_client import Counter, Histogram

# 请求计数器
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path"]
)

# 请求延迟测量
REQUEST_LATENCY = Histogram(
    "http_request_duration_ms",
    "HTTP request latency in milliseconds",
    ["method", "path"]
)