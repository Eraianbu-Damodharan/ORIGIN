from crawler import crawl_site
from request_sender import send_request
from context_detector import detect_context
from payload_engine import generate_payloads
from feature_extractor import extract_features
from rule_engine import run_rules
from anomaly_model import train_model, load_model, predict_anomaly
from evidence_engine import correlate_evidence
from scoring import calculate_confidence
from report_generator import save_report, print_report


def build_baseline_dataset(endpoints):
    feature_rows = []

    print("\n[DEBUG] All discovered endpoints:")
    for ep in endpoints:
        print(ep)

    for endpoint in endpoints:
        print(f"\n[DEBUG] Checking endpoint: {endpoint}")

        if not endpoint.get("params"):
            print("[DEBUG] Skipped - no params found")
            continue

        param = endpoint["params"][0]
        print(f"[DEBUG] Using param: {param}")

        baseline = send_request(endpoint, param_name=param, payload="normaltest123")
        attacked = send_request(endpoint, param_name=param, payload="hello")

        print("[DEBUG] Baseline status:", baseline["status_code"])
        print("[DEBUG] Attack status:", attacked["status_code"])

        features = extract_features(baseline, attacked, "hello")
        print("[DEBUG] Extracted features:", features)

        feature_rows.append(features)

    print(f"\n[INFO] Total baseline rows collected: {len(feature_rows)}")
    return feature_rows

def scan_target(target_url):
    endpoints = crawl_site(target_url, max_pages=10)
    print(f"\n[INFO] Endpoints discovered: {len(endpoints)}")

    if not endpoints:
        print("[ERROR] No usable endpoints found.")
        return

    baseline_rows = build_baseline_dataset(endpoints)
    print(f"[INFO] Baseline rows before training: {len(baseline_rows)}")

    if not baseline_rows:
        print("[ERROR] No baseline rows collected. Cannot train anomaly model.")
        return

    train_model(baseline_rows)
    model = load_model()

    results = []

    for endpoint in endpoints:
        if not endpoint.get("params"):
            continue

        param = endpoint["params"][0]
        marker = "AEGIS123MARK"

        baseline = send_request(endpoint, param_name=param, payload=marker)
        context_info = detect_context(baseline["text"], marker)
        payloads = generate_payloads(context_info["context"])

        for payload in payloads:
            attacked = send_request(endpoint, param_name=param, payload=payload)
            features = extract_features(baseline, attacked, payload)
            rule_output = run_rules(attacked, payload)
            anomaly_output = predict_anomaly(model, features)
            evidence_output = correlate_evidence(rule_output, anomaly_output, features)
            score_output = calculate_confidence(
                rule_output["rule_score"],
                anomaly_output["anomaly_score"],
                evidence_output["evidence_score"]
            )

            if score_output["confidence"] >= 0.55:
                results.append({
                    "endpoint": endpoint["url"],
                    "payload": payload,
                    "confidence": score_output["confidence"],
                    "severity": score_output["severity"],
                    "evidence": evidence_output["evidence"],
                    "recommendation": "Use input validation, output encoding, and parameterized queries"
                })

    print(f"\n[INFO] Findings collected: {len(results)}")
    save_report(results)
    print_report(results)


if __name__ == "__main__":
    target = input("Enter target URL: ").strip()
    scan_target(target)