from datetime import datetime


def current_iso_datetime():
    return datetime.now().isoformat()
