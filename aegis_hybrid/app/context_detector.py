import re


def detect_context(response_text, marker):
    if marker not in response_text:
        return {"reflected": False, "context": "unknown"}

    if f"<script>{marker}</script>" in response_text:
        return {"reflected": True, "context": "html"}

    if re.search(rf'["\']{re.escape(marker)}["\']', response_text):
        return {"reflected": True, "context": "attribute"}

    if re.search(rf'var\s+\w+\s*=\s*["\']{re.escape(marker)}["\']', response_text):
        return {"reflected": True, "context": "javascript"}

    if f"\"{marker}\"" in response_text:
        return {"reflected": True, "context": "json"}

    return {"reflected": True, "context": "unknown"}