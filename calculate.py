import pandas as pd
from datetime import datetime


def sum_of_name(entries):
    name_counts = {}
    for entry in entries:
        if entry.date.strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d'):
            if entry.name not in name_counts:
                name_counts[entry.name] = 0
            name_counts[entry.name] += entry.quantity
    return format_name_counts(name_counts)

def format_name_counts(name_counts):
    formatted_str = ""
    for name, quantity in name_counts.items():
        formatted_str += f"{name}: {quantity}\n"
    return formatted_str

def count_product(entries):
    today = datetime.today().strftime('%Y-%m-%d')
    total_quantity = sum(entry.quantity for entry in entries if entry.date.strftime('%Y-%m-%d') == today)
    return total_quantity

def sum_today(entries):
    today = datetime.today().strftime('%Y-%m-%d')
    total_thu = sum(entry.thu for entry in entries if entry.date.strftime('%Y-%m-%d') == today and entry.thu is not None)
    total_chi = sum(entry.chi for entry in entries if entry.date.strftime('%Y-%m-%d') == today and entry.chi is not None)
    return total_thu - total_chi