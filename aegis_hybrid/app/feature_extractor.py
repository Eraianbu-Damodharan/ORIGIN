from difflib import SequenceMatcher
import re


SQL_ERROR_KEYWORDS = [
    "mysql", "sql syntax", "sqlite error", "postgresql error",
    "warning", "odbc", "database error"
]


def extract_features(baseline, attacked, payload):
    baseline_text = baseline["text"]
    attacked_text = attacked["text"]

    similarity = SequenceMatcher(None, baseline_text, attacked_text).ratio()
    diff_ratio = 1 - similarity

    sql_error_count = 0
    lower_text = attacked_text.lower()
    for keyword in SQL_ERROR_KEYWORDS:
        sql_error_count += lower_text.count(keyword)

    payload_reflected = 1 if payload in attacked_text else 0
    status_changed = 1 if baseline["status_code"] != attacked["status_code"] else 0
    redirect_changed = 1 if baseline["final_url"] != attacked["final_url"] else 0

    baseline_len = max(len(baseline_text), 1)
    length_diff_ratio = abs(len(attacked_text) - len(baseline_text)) / baseline_len

    return {
        "status_changed": status_changed,
        "length_diff_ratio": length_diff_ratio,
        "response_time_diff": attacked["elapsed"] - baseline["elapsed"],
        "sql_error_count": sql_error_count,
        "payload_reflected": payload_reflected,
        "redirect_changed": redirect_changed,
        "diff_ratio": diff_ratio
    }