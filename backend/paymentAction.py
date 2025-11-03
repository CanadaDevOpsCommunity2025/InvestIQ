

def classify_transaction(amount: float, avg_amount: float, vendor: str, known_vendors: list):
    """Returns (suspicious_flag, risk_score, reason)"""
    suspicious_flag = False
    risk_score = 0
    reasons = []

    if amount > avg_amount * 3:  # unusually large spend
        risk_score += 0.5
        reasons.append("high_amount")

    if vendor not in known_vendors:
        risk_score += 0.3
        reasons.append("unknown_vendor")

    suspicious = risk_score >= 0.5
    return suspicious, round(risk_score, 2), ", ".join(reasons) or "normal"