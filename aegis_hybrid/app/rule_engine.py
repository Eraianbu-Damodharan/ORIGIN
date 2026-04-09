import re
from config import SQL_ERROR_PATTERNS, HEADERS_TO_CHECK


def run_rules(response, payload):
    matches = []
    score = 0.0
    text_lower = response["text"].lower()

    for pattern in SQL_ERROR_PATTERNS:
        if re.search(pattern, text_lower):
            matches.append(f"Matched SQL error pattern: {pattern}")
            score += 0.35

    if payload in response["text"]:
        matches.append("Payload reflected in response")
        score += 0.30

    missing_headers = []
    for header in HEADERS_TO_CHECK:
        if header not in response["headers"]:
            missing_headers.append(header)

    if missing_headers:
        matches.append(f"Missing security headers: {', '.join(missing_headers)}")
        score += 0.15

    if response["status_code"] >= 500:
        matches.append("Server error after payload injection")
        score += 0.20

    return {
        "rule_score": min(score, 1.0),
        "matches": matches
    }