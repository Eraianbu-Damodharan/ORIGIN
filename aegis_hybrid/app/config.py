SQL_ERROR_PATTERNS = [
    r"sql syntax.*mysql",
    r"warning.*mysql",
    r"unclosed quotation mark after the character string",
    r"quoted string not properly terminated",
    r"postgresql.*error",
    r"sqlite.*error"
]

XSS_PAYLOADS = {
    "html": [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>"
    ],
    "attribute": [
        "\" onmouseover=alert(1) x=\"",
        "' onfocus=alert(1) '"
    ],
    "javascript": [
        "';alert(1);//",
        "\";alert(1);//"
    ],
    "json": [
        "\"><script>alert(1)</script>"
    ],
    "unknown": [
        "<script>alert(1)</script>",
        "' OR '1'='1",
        "\" OR \"1\"=\"1"
    ]
}

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' UNION SELECT NULL--",
    "' AND SLEEP(5)--"
]

HEADERS_TO_CHECK = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "Strict-Transport-Security"
]

MODEL_PATH = "data/isolation_forest.pkl"
TIMEOUT = (5, 10)