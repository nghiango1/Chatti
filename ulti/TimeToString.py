from datetime import datetime


def timeToString(timestamp: float):
    formatted_time = datetime.fromtimestamp(
        timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
