import math
from datetime import datetime

def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
    except (TypeError, ValueError):
        return None  # or raise error

    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def get_timeline_gap(dates):
    dates = sorted(dates)
    if len(dates) < 2:
        return 0

    d1 = datetime.strptime(dates[-1], "%Y-%m-%d")
    d2 = datetime.strptime(dates[-2], "%Y-%m-%d")

    return (d1 - d2).days