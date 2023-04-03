import pytz
import datetime as dt


class Punishments:
    @staticmethod
    async def calculate_duration(duration: str):
        total_duration = 0
        punishment_removal_date = "Never"
        human_readable_duration = ""

        if duration:
            duration_factors = {'s': ('Second', 1), 'm': ('Minute', 60), 'h': ('Hour', 3600), 'd': ('Day', 86400),
                                'w': ('Week', 604800),  'mo': ('Month', 2592000), 'y': ('Year', 31536000)}

            duration_list = duration.split()

            for dur_str in duration_list:
                dur_format = dur_str[-1] if dur_str[-2:] != 'mo' else 'mo'
                if dur_format in duration_factors:
                    dur_value = dur_str[:-1]
                    if dur_value.isnumeric():
                        total_duration += int(dur_value) * duration_factors[dur_format][1]

                        # append the human-readable duration label
                        if human_readable_duration:
                            human_readable_duration += ", "
                        if int(dur_value) == 1:
                            human_readable_duration += f"1 {duration_factors[dur_format][0]}"
                        else:
                            human_readable_duration += f"{dur_value} {duration_factors[dur_format][0]}s"
                    else:
                        raise ValueError("Invalid duration, example: 1d or 1d 12h")
                else:
                    raise ValueError("Invalid duration, example: 1d or 1d 12h")

            punishment_duration = dt.timedelta(seconds=total_duration)
            punishment_removal_date = (dt.datetime.now(pytz.utc) + punishment_duration)

        return total_duration, punishment_removal_date, human_readable_duration
