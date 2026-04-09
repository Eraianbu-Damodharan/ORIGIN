def correlate_evidence(rule_output, anomaly_output, features):
    evidence = []
    evidence_score = 0.0

    if rule_output["matches"]:
        evidence.extend(rule_output["matches"])
        evidence_score += 0.4

    if anomaly_output["anomaly_label"] == 1:
        evidence.append("Anomaly model flagged the response")
        evidence_score += 0.3

    if features["payload_reflected"]:
        evidence.append("Injected payload reflected in response")
        evidence_score += 0.15

    if features["diff_ratio"] > 0.30:
        evidence.append("Large response difference from baseline")
        evidence_score += 0.10

    if features["response_time_diff"] > 2:
        evidence.append("Significant response delay observed")
        evidence_score += 0.05

    return {
        "evidence_score": min(evidence_score, 1.0),
        "evidence": evidence
    }