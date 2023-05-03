import argparse
from modules_buy_sell import sell_product, buy_product
import csv
from mod_reports import report_sold_bought, report_inventory, report_revenue, report_profit
from mod_small_functions import get_current_date
from create_timewindow import create_timewindow
import matplotlib.pyplot as plt

print('')
print('===============================================================================================================================================================')
print('================================================ Running super.py ============================================================================================')
print('===============================================================================================================================================================')
print('')


# ############################################################################
# ################# ARGPARSE SECTION  ########################################

# create the main parser
parser = argparse.ArgumentParser(description='Program for Supermarket Administration')
parser.add_argument('--advance-days'    , help='the amount of days you want to skip forward (a negative number will skip backward)', type=int)
parser.add_argument('--current-date'    , help='returns the current date used in the program', action="store_true")
parser.add_argument('--set-date'        , help='wit this command you can enter a specific date that you like to program to use as the current date')

# create subparsers
subparsers = parser.add_subparsers(dest='command', title="Subcommands")

# create the parser for the 'buy' subcommand
buy_parser = subparsers.add_parser('buy'    , help='with this subcommant you can add a product to bought.csv')
buy_parser.add_argument('--name', '-n'      , help='name off the bought product', required=True)
buy_parser.add_argument('--price', '-p'     , help='price off the bought product', required=True)
buy_parser.add_argument('--exp', '-x'       , help='expitation date off the bought product', required=True)
buy_parser.add_argument('--buy-date', '-bd' , help='date when you bought the bought product (if different from "today")')

# create the parser for the 'sell' subcommand
buy_parser = subparsers.add_parser('sell'   , help='with this subcommant you can add a product to sold.csv')
buy_parser.add_argument('--name', '-n'      , help='name off the sold product', required=True)
buy_parser.add_argument('--price', '-p'     , help='price off the sold product', required=True)
buy_parser.add_argument('--sell-date', '-sd', help='date when you sold the product (if different from "today")')

# create the parser for the 'report' subcommand
report_parser = subparsers.add_parser('report', help='with this subcommant you can create different kind of REPORTS')
report_parser.add_argument('type'           , help='options: inventory, revenue, profit, bought, sold, expired', )#choices=['inventory', 'revenue', 'profit', 'bought', 'sold', 'expired'])
report_parser.add_argument('--now'    , '-n', help='analysis based on: all data untill the current date (default, used if no optional input is provided)', action="store_true")
report_parser.add_argument('--today'  , '-t', help='analysis based on: data on the current date of the program'                               , action="store_true")
report_parser.add_argument('--yesterday'    , help='analysis based on: data of yesterday (day before current date of the program)'                 , action="store_true")
report_parser.add_argument('--date'         , help='analysis based on: data of a specific date: yyyy-mm-dd')
report_parser.add_argument('--timewindow'   , help='analysis based on: data in timewindow; input start and end dates: yyyy-mm-dd yyyy-mm-dd (the end date day is included in the analysis)', nargs=2)
report_parser.add_argument('--month'        , help='analysis based on: data in specific month; input a month & year: yyyy-mm')
report_parser.add_argument('--year'         , help='analysis based on: data in specific year; input a year')
report_parser.add_argument('--save-inv-tab' , help='saves the inventory summary table (only works with the inventory report)', action="store_true")
report_parser.add_argument('--save-inv-bar' , help='saves the inventory summary bar plot (only works with the inventory report)', action="store_true")

args = parser.parse_args()
# print(args)

# print errors and exit if wrong input is provided
if args.command == 'report':
    if args.type == 'inventory':
        if args.timewindow is not None or args.month is not None or args.year is not None or args.today is not False or args.yesterday is not False:
            print('===============================================================================')
            print('Error: For "report inventory" --yesterday/--today/--timewindow/--month/--year does not work')
            print('       because inventory cannot be calculated for a time period')
            print('       Pelease input --date or --now (default) ')
            print('===============================================================================')
            exit()
    elif args.save_inv_tab is not False or args.save_inv_bar is not False:
        print('===============================================================================')
        print('Error: Only for "report inventory" a TABLE or a BAR FIGURE can be saved')
        print('===============================================================================')
        exit()


# ############################################################################
# ################# LOAD/SET CURRENT DATE and TIMEWINDOW #####################

# LOAD CURRENT DATE
current_date_file = 'current_date.txt'
current_date_str = get_current_date(current_date_file)
print('Current date in program: ' + current_date_str)

# ADVANCE/SET DAYS IF REQUESTED
if args.advance_days is not None:
    current_date_str_new = get_current_date(current_date_file, args.advance_days)
    print('New date in program = ' + current_date_str_new + ' (old date = ' + current_date_str + ')')
    current_date_str = current_date_str_new
if args.set_date is not None:
    current_date_str_new = args.set_date
    print('New date in program = ' + current_date_str_new + ' (old date = ' + current_date_str + ')')
    current_date_str = current_date_str_new
if args.set_date is not None or args.advance_days is not None:
    with open('current_date.txt', 'w', newline='') as csvfile:
        writer_object = csv.writer(csvfile)
        writer_object.writerow([current_date_str_new])
print('')

# Check if time window is provided. If not, create a timewindow from 2000-01-01 (an arbitrary date before the supermarket started) until the current date.
timewindow = create_timewindow(args, current_date_str)


# ############################################################################
# ######################## BUY/SELL A PRODUCT ################################
if args.command == 'buy':
    if args.buy_date:
        buy_product(args, args.buy_date, print_yes='yes')        
    else:
        buy_product(args, current_date_str,print_yes='yes')
# breakpoint()
if args.command == 'sell':
    if args.sell_date:
        timewindow    = ['2000-01-01', args.sell_date]
        sell_product(args, timewindow, args.sell_date, print_yes='yes')       
    else:
        sell_product(args, timewindow, current_date_str, print_yes='yes')


# ############################################################################
# ######################## MAKE A REPORT ################################
if args.command == 'report':
    if args.type == 'sold' or args.type == 'bought':
        report_sold_bought(args.type, timewindow)
    elif args.type == 'inventory':
        a, table = report_inventory(timewindow)
    elif args.type == 'revenue':
        report_revenue(timewindow)
    elif args.type == 'profit':
        report_profit(timewindow)
# breakpoint()

# extra functionality for inventory report (save csv table &  bar plot)
if args.command == 'report':
    if args.type == 'inventory':
        if args.save_inv_tab is True:
            save_table_name = 'TABLE-' + timewindow[1] + '.csv'
            with open(save_table_name, 'w', newline='') as csvfile:
                writer_object = csv.writer(csvfile)
                for line in table:
                    writer_object.writerow(line)
        if args.save_inv_bar is True:
            fig, ax = plt.subplots()
            products = []
            counts = []
            table_bar = table[1:]
            for product in table_bar:
                products.append(product[0])
                counts.append(product[1])
            ax.bar(products, counts)  
            ax.set_ylabel('Amount in stock')
            ax.set_title('Shop Inventory: ' + timewindow[1])
            name_bar = 'BARPLOT-' + timewindow[1] + '.png'
            plt.savefig(name_bar)
            plt.show()

print('')
print('============ END OF PROGRAM ====================')
print('')
