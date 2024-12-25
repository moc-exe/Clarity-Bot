from datetime import datetime

def get_curr_timestamp() -> str:
    '''returns currtime in human readable format'''
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def unix_time_to_str(unix_timestamp:int) -> str:
    '''transforms unix timestamp into human readable format'''
    return datetime.fromtimestamp(unix_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

