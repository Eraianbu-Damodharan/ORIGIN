def calculate_confidence(rule_score, anomaly_score, evidence_score):
    confidence = (
        0.45 * rule_score +
        0.25 * anomaly_score +
        0.30 * evidence_score
    )

    if confidence >= 0.65:
        severity = "High"
    elif confidence >= 0.40:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "confidence": round(confidence, 3),
        "severity": severity
    }