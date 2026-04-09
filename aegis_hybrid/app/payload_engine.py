from config import XSS_PAYLOADS, SQLI_PAYLOADS


def generate_payloads(context):
    payloads = []
    payloads.extend(XSS_PAYLOADS.get(context, XSS_PAYLOADS["unknown"]))
    payloads.extend(SQLI_PAYLOADS)
    return payloads