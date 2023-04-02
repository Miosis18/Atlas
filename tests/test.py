import datetime

input_duration = input("Enter duration (e.g. 1s, 1m, 1h, 1d, 1w, 1mo, 1y): ")

duration_factors = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'mo': 2592000, 'y': 31536000}

duration_list = input_duration.split()
total_duration = 0
for duration_str in duration_list:
    duration_format = duration_str[-1] if duration_str[-2:] != 'mo' else 'mo'
    if duration_format in duration_factors:
        duration_value = duration_str[:-1]
        if duration_value.isnumeric():
            total_duration += int(duration_value) * duration_factors[duration_format]
        else:
            print("Invalid duration value:", duration_value)
            break
    else:
        print("Invalid duration format:", duration_format)
        break

ban_duration = datetime.timedelta(seconds=total_duration)

print(datetime.datetime.utcnow() + ban_duration)
