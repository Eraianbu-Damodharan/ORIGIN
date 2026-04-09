def correlate_evidence(rule_output, anomaly_output, features):
    evidence = []
    evidence_score = 0.0

    # Rule-based evidence
    if rule_output.get("matches"):
        evidence.extend(rule_output["matches"])
        evidence_score += 0.35

    # ML anomaly evidence
    if anomaly_output.get("anomaly_label") == 1:
        evidence.append("Anomaly model flagged the response")
        evidence_score += 0.25

    # Reflection evidence
    if features.get("payload_reflected", 0):
        evidence.append("Injected payload reflected in response")
        evidence_score += 0.10

    # Response diff evidence
    if features.get("diff_ratio", 0) > 0.30:
        evidence.append("Large response difference from baseline")
        evidence_score += 0.15

    # Delay-based evidence
    if features.get("response_time_diff", 0) > 2:
        evidence.append("Significant response delay observed")
        evidence_score += 0.15

    # SQL-specific evidence
    if features.get("sql_error_count", 0) > 0:
        evidence.append("SQL-related error keywords detected")
        evidence_score += 0.20

    # Status change evidence
    if features.get("status_changed", 0) == 1:
        evidence.append("Response status changed after injection")
        evidence_score += 0.15

    return {
        "evidence_score": min(evidence_score, 1.0),
        "evidence": evidence
    }