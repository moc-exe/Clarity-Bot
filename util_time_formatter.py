from datetime import datetime
def get_curr_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")