import pandas as pd

def get_string_amount(value):
    return '{:,}'.format(value).replace(',', ' ')

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