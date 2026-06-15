import pandas as pd


def check_odd_hour(transaction_time):
    hour = transaction_time.hour

    if hour >= 0 and hour <= 5:
        return 15

    return 0


def check_large_amount(amount, avg_amount):

    if amount > avg_amount * 5:
        return 25

    return 0


def check_new_device(current_device, known_devices):

    if current_device not in known_devices:
        return 30

    return 0