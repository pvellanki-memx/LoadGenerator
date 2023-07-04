import random
import string
import time

def validate_execution_report(exec_report, order_qty, symbol, order_type, tif):
    # Validate OrderQty
    assert exec_report.getField(32) == str(order_qty), "Execution Report OrderQty mismatch"

    # Validate Symbol
    assert exec_report.getField(55) == symbol, "Execution Report Symbol mismatch"

    # Validate OrdType
    assert exec_report.getField(40) == order_type, "Execution Report OrdType mismatch"

    # Validate TimeInForce
    assert exec_report.getField(59) == tif, "Execution Report TimeInForce mismatch"

def replace_placeholders(message, placeholders):
    for placeholder, value in placeholders.items():
        message = message.replace(placeholder, value)
    return message

def generate_clOrdID():
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return rand_str

def calculate_sending_time():
    return time.strftime("%Y%m%d-%H:%M:%S.%f")[:-3]

def calculate_checksum(message):
    checksum = sum(ord(c) for c in message) % 256
    return str(checksum).zfill(3)
