import json
import os


def save_report(results, path="data/scan_results.json"):
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def print_report(results):
    for item in results:
        print("=" * 60)
        print("Endpoint:", item["endpoint"])
        print("Payload:", item["payload"])
        print("Confidence:", item["confidence"])
        print("Severity:", item["severity"])
        print("Evidence:")
        for ev in item["evidence"]:
            print("-", ev)
        print("Recommendation:", item["recommendation"])