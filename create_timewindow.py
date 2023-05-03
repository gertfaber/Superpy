from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

def create_timewindow(args, current_date_str):
    
    if not hasattr(args, 'timewindow'):
        timewindow = ['2000-01-01', current_date_str]
    else:
        if args.timewindow is None:
            timewindow = ['2000-01-01', current_date_str]
        else:
            timewindow = args.timewindow

    if hasattr(args, 'date'):
        if args.date:
            if args.type == 'inventory': # inventory cannot be calculated for one day
                timewindow = ['2000-01-01', args.date]
            else:
                timewindow    = [args.date, args.date]

    # breakpoint()

    if hasattr(args, 'today'):
        if args.today:
            timewindow    = [current_date_str, current_date_str]

    if hasattr(args, 'yesterday'):
        if args.yesterday:        
            current_date  = datetime.strptime(current_date_str,"%Y-%m-%d")
            yesterday     = current_date + timedelta(days=-1)
            yesterday_str = yesterday.strftime("%Y-%m-%d")
            timewindow    = [yesterday_str, yesterday_str]

    if hasattr(args, 'month'):
        if args.month:
            Start_timewindow = datetime.strptime(args.month,"%Y-%m")
            End_timewindow   = Start_timewindow + relativedelta(months=1)+timedelta(days=-1)
            timewindow       = [Start_timewindow.strftime("%Y-%m-%d"), End_timewindow.strftime("%Y-%m-%d")]

    if hasattr(args, 'year'):
        if args.year:
            Start_timewindow = datetime.strptime(args.year,"%Y")
            End_timewindow   = Start_timewindow + relativedelta(years=1)+timedelta(days=-1)
            timewindow       = [Start_timewindow.strftime("%Y-%m-%d"), End_timewindow.strftime("%Y-%m-%d")]
    
    return timewindow