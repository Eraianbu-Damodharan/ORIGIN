def calculate_confidence(rule_score, anomaly_score, evidence_score):
    confidence = (
        0.35 * rule_score +
        0.30 * anomaly_score +
        0.35 * evidence_score
    )

    if confidence >= 0.80:
        severity = "High"
    elif confidence >= 0.55:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "confidence": round(confidence, 3),
        "severity": severity
    }