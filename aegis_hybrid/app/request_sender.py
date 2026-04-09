import requests
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

def send_request(endpoint, param_name=None, payload=None):
    url = endpoint["url"]
    method = endpoint["method"].upper()

    start = time.time()

    try:
        if method == "GET":
            params = {}
            if param_name and payload is not None:
                params[param_name] = payload
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=(5, 10),
                allow_redirects=True
            )
        else:
            data = {}
            if param_name and payload is not None:
                data[param_name] = payload
            response = requests.post(
                url,
                data=data,
                headers=HEADERS,
                timeout=(5, 10),
                allow_redirects=True
            )

        elapsed = time.time() - start

        return {
            "status_code": response.status_code,
            "text": response.text,
            "headers": dict(response.headers),
            "elapsed": elapsed,
            "final_url": response.url
        }

    except Exception as e:
        return {
            "status_code": 0,
            "text": str(e),
            "headers": {},
            "elapsed": time.time() - start,
            "final_url": url
        }