import pandas as pd
from datetime import datetime, timedelta

def get_string_amount(value):
    return '{:,}'.format(value).replace(',', ' ')

def older_id(dates_list):
    older = datetime.strptime(dates_list[0], '%d/%m/%Y')
    format_dates = []
    for date in dates_list :
        date = datetime.strptime(date, '%d/%m/%Y')
        format_dates.append(date)
        if date < older:
            older = date
    return format_dates.index(older)

def newer_id(dates_list):
    newer = datetime.strptime(dates_list[0], '%d/%m/%Y')
    format_dates = []
    for date in dates_list :
        date = datetime.strptime(date, '%d/%m/%Y')
        format_dates.append(date)
        if date > newer:
            newer = date
    return format_dates.index(newer)

def in_range_id(dates_list, start: datetime, end: datetime):
    in_range = []
    for i in range(len(dates_list)):
        date = datetime.strptime(dates_list[i], '%d/%m/%Y')
        if start <= date <= end:
            in_range.append(i)
    return in_range

def make_df(headings, rows):
        data = {}
        for i in range(0, len(headings)):
            col = []
            for j in range(0, len(rows)):
                row = rows[j]
                try:
                    col.append(float(row[i]))
                except ValueError:
                    col.append(row[i])
                except IndexError:
                    col.append('')
            data[headings[i]] = col
        return pd.DataFrame(data)

def min_col_df(df : pd.DataFrame, column : int, ignore_non_numeric_error=True):
     values = list(df.iloc[:, column-1])
     for value in values:
        try:
            float(value)
        except:
            values.remove(value)
            if not ignore_non_numeric_error:
                raise ValueError 
     return min(values)

def max_col_df(df : pd.DataFrame, column : int, ignore_non_numeric_error=True):
     values = list(df.iloc[:, column-1])
     for value in values:
        try:
            float(value)
        except:
            values.remove(value)
            if not ignore_non_numeric_error:
                raise ValueError 
     return max(values)