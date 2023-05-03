from mod_read_csv import read_csv
from tabulate import tabulate
from mod_small_functions import calc_days_diff, Extract
from rich import print


def report_revenue(timewindow):
    # REVENUE / OMZET (optellen van bought items)
    # if args.command == 'revenue':
    csv_name_sold = 'sold.csv' 
    print('============== ALL SOLD products used in REVENUE calculation (timewindow: ' + str(timewindow) + ')=================')
    csv_data_sold = read_csv(csv_name_sold, 'yes', timewindow)   
    revenue = 0
    for line in csv_data_sold[1:]:
        revenue += float(line[6])
    print('Revenue: €' + str(revenue))
    print('')
    print('============================================================')


def report_sold_bought(type, timewindow):
    if type == 'sold':  # for selling it is just printing the csv file
        print('                                                     ')    
        print('=============== SOLD in timewindow: ' + str(timewindow) + ' =====================')
        cvs_name_sold = 'sold.csv'
        read_csv(cvs_name_sold, 'yes', timewindow)
    elif type == 'bought':  # for bought extra info is claculated and added to the table:
        cvs_name_bought = 'bought.csv'
        csv_data_bought = read_csv(cvs_name_bought, 'no', timewindow)
        cvs_name_sold = 'sold.csv'
        csv_data_sold_all = read_csv(cvs_name_sold, 'no') 

        # Extract all the bought_ids of the sold products (also if sold in the future)
        try:
            sold_bougth_ids = Extract(csv_data_sold_all[1:])
        except: 
            sold_bougth_ids = []  

        # Adding selling date if the product has been sold (also if in the future)
        product_line = 1
        for product_bought in csv_data_bought[1:]:
            if sold_bougth_ids.count(int(product_bought[0])):  # heck if product has been sold
                id_bought = product_bought[0]
                # find product again in sold list and extract sell_date
                for product_sold in csv_data_sold_all:
                    if product_sold[1] == id_bought:
                        sell_date = product_sold[4]
                        csv_data_bought[product_line].append(sell_date)
            else:
                csv_data_bought[product_line].append(' ')  # for products that have not been expired
            product_line += 1

        # calculating the amount of days that the product expired
        for i_line in range(1, len(csv_data_bought)):
            line = csv_data_bought[i_line]
            days_expired = calc_days_diff(timewindow[1], line[4])
            if days_expired > 0:
                csv_data_bought[i_line].append('Expired: ' + str(days_expired) + ' days')
            else:
                csv_data_bought[i_line].append(' ')

        # Adding extra variables to table and print
        csv_data_bought[0].append('sell_date')
        csv_data_bought[0].append('expired with respect to end timewindow')
        print('                                                     ')
        print('=============== BOUGHT in timewindow: ' + str(timewindow) + ' =====================')
        print(tabulate(csv_data_bought[1:], csv_data_bought[0], tablefmt="grid"))


def report_inventory(timewindow, print_on='yes'):
    # inventory is bought items minus sold items
    # Open Sold CVS and extract the bought IDs

    # printing bought and sold tables for the specified timewindow
    cvs_name = 'bought.csv'
    print('                                                     ')    
    print('=============== BOUGHT up to and including:' + timewindow[1] + ' =====================')
    csv_data_bought = read_csv(cvs_name, 'yes', timewindow=['2000-01-01', timewindow[1]])
    cvs_name = 'sold.csv'
    print('                                                     ')    
    print('=============== SOLD up to and including: ' + timewindow[1] + ' =====================')
    csv_data_sold = read_csv(cvs_name, 'yes', timewindow=['2000-01-01', timewindow[1]]) # only use the end date

    # Extract all the bought_ids of the sold products (not if sold in the future)
    try:
        sold_bougth_ids = Extract(csv_data_sold[1:])
    except:
        sold_bougth_ids = []  

    # Copy only products which have been sold already
    csv_data_bought_new = [csv_data_bought[0]]
    for product_bought in csv_data_bought[1:]:
        bought_id = product_bought[0]
        if sold_bougth_ids.count(int(bought_id)) < 1:
            csv_data_bought_new.append(product_bought)
    csv_data_bought = csv_data_bought_new[:]  # overwrite old variable with new one

    # Add expiration data to the table
    csv_data_bought[0].append('days expired')
    for i_line in range(1, len(csv_data_bought)):
        line = csv_data_bought[i_line]
        days_expired = calc_days_diff(timewindow[1], line[4])
        if days_expired > 0:
            csv_data_bought[i_line].append(days_expired)
        else:
            csv_data_bought[i_line].append(' ')

    # print store inventory (including expired products)
    if print_on == 'yes':
        print('                                                     ')
        print('=============== Store inventory (bought list minus sold list) up to and including: ' + timewindow[1] + ' =====================')
        print(tabulate(csv_data_bought[1:], csv_data_bought[0], tablefmt="grid"))

    # Inventory: Copy only non-expired products
    csv_data_bought_not_exp = []
    csv_data_bought_not_exp.append(csv_data_bought[0][:5])
    for i_line in csv_data_bought[1:]:
        if i_line[5] == ' ':  # if not expired: append line
            csv_data_bought_not_exp.append(i_line[:5])

    # print store inventory (without expired products)
    if print_on == 'yes':
        print('                                                     ')    
        print('=============== Store inventory (expired products removed) up to and including: ' + timewindow[1] + ' =====================')
        print(tabulate(csv_data_bought_not_exp[1:], csv_data_bought_not_exp[0], tablefmt="grid"))

    # calculating inventory summary
    product_names = []
    for product in csv_data_bought_not_exp[1:]:  # extracting product names
        product_names.append(product[1])

    product_types = list(set(product_names))  # make a set to remove dupicates
    product_types.sort()  # sort the list
    inventory_summary = [['product_name', 'count']]
    for product_type in product_types:  #creat table
        inventory_summary.append([product_type, product_names.count(product_type)])

    if print_on == 'yes':  # print inventory summary table
        print('                                                     ')    
        print('=============== SUMMARY Store inventory (excluding expired products) up to and including: ' + timewindow[1] + ' =====================')
        print(tabulate(inventory_summary[1:], ['product_name', 'Count'], tablefmt="grid"))

    return csv_data_bought_not_exp[1:], inventory_summary


def report_profit(timewindow):
    # PROFIT ON SOLD PRODUCTS

    # print table with sold products
    print('============== PROFIT SOLD products in timewindow: ' + str(timewindow) + ' =================')
    csv_name_sold = 'sold.csv' 
    csv_data_sold = read_csv(csv_name_sold, 'yes', timewindow)
    profit_sold_products = 0

    # print the total profit of all sold products
    for line in csv_data_sold[1:]:  # sum profit (sell_price-buy_price) over products
        profit_sold_products += float(line[6]) - float(line[5])
    print('Profit on Sold products: ' + str(profit_sold_products) + ' Euro')
    print('============================================================')

    # EXPIRED FOODS / LOSS CALCULATION
    csv_name_bought = 'bought.csv'
    csv_data_bought = read_csv(csv_name_bought, 'no', timewindow)
    csv_name_sold = 'sold.csv'
    csv_data_sold = read_csv(csv_name_sold, 'no', timewindow)

    # extracting the id numbers of the sold items
    id_sold_items = []
    csv_data_sold_all = read_csv(csv_name_sold, 'no', ['2000-01-01', timewindow[1]]) # also the bought_id of the products sold before/after the timewindow
    for line in csv_data_sold_all[1:]: # extract (bought) id numbers in the sold list
        id_sold_items.append(int(line[1]))

    Exp_Table_not_sold = []
    Loss_total = 0
    for line in csv_data_bought[1:]: # loop through bought list to fin expired foods
        id_bought = int(line[0])
        exp_date_str = line[4]

        days_expired = calc_days_diff(exp_date_str,timewindow[1])
        line.append('')

        if days_expired < 0:  # find expired foods
            if (id_bought in id_sold_items): 
                line[5]='yes'
            else:
                line[5]='no'

        if days_expired < 0 and (id_bought not in id_sold_items):  # find expired foods that have not been sold 
            Exp_Table_not_sold.append(line)
            Loss_total += float(line[3])


    header = csv_data_bought[0]
    header.append('sold?')

    print('============== Overview all expired products that have not been sold (loss) in timewindow: ' + str(timewindow) + ' =================')
    print(tabulate(Exp_Table_not_sold[:], csv_data_bought[0], tablefmt="grid"))
    print('Total loss: ' + str(Loss_total) + ' Euros')
    print('============================================================')

    print('Profit on Sold products: ' + str(profit_sold_products) + ' Euro')
    print('Loss expired products  : ' + str(Loss_total) + ' Euro')
    print('Final Provit           : ' + str(profit_sold_products-Loss_total) + ' Euro')
