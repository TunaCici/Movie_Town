import datetime

def get_str_time() -> str:
    hour = datetime.datetime.now().hour

    if 0 <= hour and hour < 6:
        return "Night"
    elif 6 <= hour and hour < 12:
        return "Morning"
    elif 12 <= hour and hour < 18:
        return "Afternoon"
    elif 18 <= hour and hour < 24:
        return "Evening"
    else:
        return "Day"