def normalize(value, min_value, max_value):
    if max_value == min_value:
        return 0

    return ((value - min_value) / (max_value - min_value)) * 100


def calculate_risks(asset, traffic_min, traffic_max,
                    accident_min, accident_max):

    condition_risk = 100 - float(asset["condition"])

    age_risk = min(
        (float(asset["age"]) / 30) * 100,
        100
    )

    traffic_risk = normalize(
        float(asset["traffic"]),
        traffic_min,
        traffic_max
    )

    accident_risk = normalize(
        float(asset["accidents"]),
        accident_min,
        accident_max
    )

    environmental_risk = float(asset["environmental_risk"])

    risk_score = (
        0.35 * condition_risk
        + 0.15 * age_risk
        + 0.15 * traffic_risk
        + 0.15 * accident_risk
        + 0.20 * environmental_risk
    )

    if risk_score >= 80:
        classification = "Critical"
    elif risk_score >= 60:
        classification = "High"
    elif risk_score >= 40:
        classification = "Moderate"
    else:
        classification = "Low"

    return {
        "condition_risk": round(condition_risk, 2),
        "age_risk": round(age_risk, 2),
        "traffic_risk": round(traffic_risk, 2),
        "accident_risk": round(accident_risk, 2),
        "environmental_risk": round(environmental_risk, 2),
        "risk_score": round(risk_score, 2),
        "classification": classification
    }
