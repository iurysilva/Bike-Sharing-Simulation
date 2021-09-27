from datetime import datetime


def get_difference_in_minutes(initial_time, end_time):
    date_format_str = '%m/%d/%Y %H:%M'
    initial_time = datetime.strptime(initial_time, date_format_str)
    end_time = datetime.strptime(end_time, date_format_str)
    duration = end_time - initial_time
    return duration.total_seconds() / 60

def get_date_str(time):
    date_format_str = '%m/%d/%Y %H:%M'
    date = datetime.strptime(time, date_format_str)
    date.strftime('%m/%d/%Y')
    return date
