import csv
from tabulate import tabulate
from mod_small_functions import calc_days_diff
from rich import print


# READ CSV FILES and PRINT TABLE (optional)
def read_csv(csv_name, print_csv='yes', timewindow=['2000-01-01', '9999-99-99']):
    with open(csv_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        csv_data = list(reader)

    # select only the products that are sold/bought within the timewindow
    if timewindow != ['2000-01-01', '9999-99-99']:
        csv_data_new = [csv_data[0]]
        if csv_data[0][0] == 'sold_id':
            index = 4
        elif csv_data[0][0] == 'bougth_id':
            index = 2

        for line in csv_data[1:]:  # date sold[index 4] or bought[index 3] 
            date_sold_or_bought = line[index]   
            date_after_start_window = calc_days_diff(date_sold_or_bought, timewindow[0]) >= 0
            date_before_end_window = calc_days_diff(timewindow[1], date_sold_or_bought) >= 0
            if date_after_start_window and date_before_end_window:
                csv_data_new.append(line)

        csv_data = csv_data_new[:]        

    if print_csv == 'yes':
        print(tabulate(csv_data[1:], csv_data[0], tablefmt="grid"))
        print('=============== ============== =====================')
        print('                                                     ')
    return csv_data
