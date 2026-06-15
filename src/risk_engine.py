from src.rules import (
    check_odd_hour,
    check_large_amount,
    check_new_device
)


def calculate_risk(row, avg_amount, known_devices):

    score = 0
    reasons = []

    odd_hour_score = check_odd_hour(row["timestamp"])

    if odd_hour_score:
        score += odd_hour_score
        reasons.append("Odd Hour")

    amount_score = check_large_amount(
        row["amount"],
        avg_amount
    )

    if amount_score:
        score += amount_score
        reasons.append("Large Amount")

    device_score = check_new_device(
        row["device_id"],
        known_devices
    )

    if device_score:
        score += device_score
        reasons.append("New Device")

    return score, reasons