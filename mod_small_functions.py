from datetime import timedelta, datetime
import csv


def get_current_date(current_date_file, advance_days=0):
    f = open(current_date_file, "r")
    current_date_str = f.readline()
    f.close()

    current_date = datetime.strptime(current_date_str[:10],"%Y-%m-%d")
    new_date = current_date + timedelta(days=advance_days)
    new_date_str = new_date.strftime("%Y-%m-%d")

    with open('current_date.txt', 'w', newline='') as csvfile:
        writer_object = csv.writer(csvfile)
        writer_object.writerow([new_date_str])

    return new_date_str


def calc_days_diff(date_str1, date_str2):
    # breakpoint()
    date1      = datetime.strptime(date_str1, "%Y-%m-%d")
    date2      = datetime.strptime(date_str2, "%Y-%m-%d")
    delta_date = date1-date2
    return delta_date.days


def Extract(lst):
    return [(int(item[1])) for item in lst]
