import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

def crawl_site(start_url, max_pages=15):
    visited = set()
    to_visit = [start_url]
    endpoints = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        try:
            response = requests.get(url, headers=HEADERS, timeout=(5, 10), allow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"[ERROR] Failed to crawl {url}: {e}")
            continue

        parsed = urlparse(url)
        query_params = list(parse_qs(parsed.query).keys())

        if query_params:
            endpoints.append({
                "url": url,
                "method": "GET",
                "params": query_params
            })

        for form in soup.find_all("form"):
            action = form.get("action")
            method = form.get("method", "GET").upper()
            form_url = urljoin(url, action) if action else url

            inputs = []
            for inp in form.find_all(["input", "textarea", "select"]):
                name = inp.get("name")
                input_type = inp.get("type", "").lower()

                if name and input_type not in ["submit", "button", "reset", "file", "hidden"]:
                    inputs.append(name)

            if inputs:
                endpoints.append({
                    "url": form_url,
                    "method": method,
                    "params": inputs
                })

        for a in soup.find_all("a", href=True):
            next_url = urljoin(url, a["href"])
            if urlparse(next_url).netloc == urlparse(start_url).netloc:
                if next_url not in visited and next_url not in to_visit:
                    to_visit.append(next_url)

    print("\n[INFO] Final endpoint list:")
    for ep in endpoints:
        print(ep)

    return endpoints    