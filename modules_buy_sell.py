import csv
from mod_read_csv import read_csv
from mod_reports import report_inventory, report_sold_bought
from mod_small_functions import calc_days_diff
from rich import print


def buy_product(args, current_date_str, print_yes='no'): 
    cvs_name_bought = 'bought.csv'

    if print_yes == 'yes':
        print('')
        print('--------------------------------------------------------------')
        print('------------------------OLD sold.csv--------------------------')
        report_sold_bought('bought', ['2000-01-01', current_date_str])

    with open(cvs_name_bought, 'a+', newline='') as csvfile:
        csvfile.seek(0)
        reader = csv.reader(csvfile)
        list_reader = list(reader)
        writer_object = csv.writer(csvfile)
        List = [int(list_reader[-1][0])+1, args.name, current_date_str, args.price, args.exp]
        list_reader.append(List)
        writer_object.writerow(List)

    if print_yes == 'yes':
        print('')
        print('----------------------------------------------------------------------')
        print('-----------------UPDATED sold.csv (after adding product)------------------')
        report_sold_bought('bought', ['2000-01-01', current_date_str])


def sell_product(args, timewindow, current_date_str, print_yes='no'):
    csv_name_sold = 'sold.csv'

    # check if available in inventory at the time of selling
    Inventory, summary = report_inventory(timewindow, print_on='yes')
    match = 0

    # because it could be possible that the product has been slod aleady in 
    # the future, whe should double check that by checking all the IDs of
    # all the sold products (also in the future)
    # extracting bought_id of the sold products

    csv_data_sold_all = read_csv(csv_name_sold, 'no')
    sold_bought_id = []
    for sold_poduct_all in csv_data_sold_all[1:]:
        sold_bought_id.append(sold_poduct_all[1])

    exp_date = '3000-01-01'  # initial date far in the furure
    for product_inventory in Inventory:
        bought_id = product_inventory[0]

        # check if product is:
        # 1. in inventory (expired produscts have been removed already)
        # 2. has not been sold yet (also not in the future)
        if args.name == product_inventory[1] and sold_bought_id.count(bought_id) < 1:                
            exp_date2 = product_inventory[4]
            # sell the product that expires the soonest
            if calc_days_diff(exp_date, exp_date2) > 0:  # if next product expires sooner, overwrite with this one
                exp_date = exp_date2
                sold_product = product_inventory
                match = 1

    if match ==1:
        sold_product_buy_id     = sold_product[0]
        sold_product_buy_date   = sold_product[2]
        sold_product_buy_price  = sold_product[3]   
        sold_product_buy_expdate= sold_product[4]   
        csv_data_sold = read_csv(csv_name_sold, 'no', timewindow)

        if print_yes == 'yes':
            print('                                                     ')    
            print('=============== OLD SOLD TABLE up to and including: ' + timewindow[1] + ' =====================')
            read_csv(csv_name_sold, 'yes', timewindow)

        try:
            new_sold_id = int(csv_data_sold_all[-1][0]) + 1
        except:
            new_sold_id = 1          
        # breakpoint()
        List = [new_sold_id, sold_product_buy_id, args.name, sold_product_buy_date, current_date_str, sold_product_buy_price, args.price, sold_product_buy_expdate]
        csv_data_sold.append(List)

        with open(csv_name_sold, 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            writer_object.writerow(List) 

        if print_yes == 'yes':
            print('                                                     ')    
            print('=============== UPDATED SOLD TABLE up to and including: ' + timewindow[1] + ' =====================')
            read_csv(csv_name_sold, 'yes', timewindow)
            print('=============== ============== =====================')
            print('                                                     ')

    if match == 0:
        print('Error: product that you are trying to sell is not in the inventory list (check inventory summary table above),')
        print('       or has been sold in the future (check the SOLD table above)!')
