import pandas as pd
from math import ceil
from PyQt5.QtWidgets import QTableWidgetItem as QTI
from PyQt5.QtWidgets import QTableWidget
from os.path import basename


def dict_to_dataframe(d: dict):
    return pd.DataFrame.from_dict(d)


def to_series(n, col_name):
    return pd.Series(data=n, name=col_name)


def round_to_odd(d):
    return ceil(d / 2) * 2 + 1


def dict_to_table(d: dict, table: QTableWidget):
    columns = len(d.keys())
    rows = max([len(d.get(k)) for k in d.keys()])

    tab = table
    tab.setRowCount(rows)
    tab.setColumnCount(columns)
    horheaders = []
    for i, k in enumerate(sorted(d.keys())):
        horheaders.append(k)
        for j, el in enumerate(d[k]):
            newitem = QTI(el)
            tab.setItem(j, i, newitem)
    tab.setHorizontalHeaderLabels(horheaders)


def table_to_dict(table: QTableWidget):
    d = {}
    tab = table
    for n in range(tab.columnCount()):
        k = tab.horizontalHeaderItem(n).text()
        d[k] = [None] * tab.rowCount()
        for m in range(tab.rowCount()):
            d[k][m] = tab.item(m, n).text()
    return d


def insert_column(table: QTableWidget, txt):
    item = QTI(txt)
    last_col = table.columnCount()
    table.insertColumn(last_col)
    table.setHorizontalHeaderItem(last_col, item)


def get_filename(p: str):
    return basename(p)


def flatten(t):
    return [item for sublist in t for item in sublist]


def list_to_lower(t):
    return [s.lower() for s in t]


def remove_duplicates(t):
    return list(set(t))


def maybeMakeNumber(s):
    """Returns a string 's' into a integer if possible, a float if needed or
    returns it as is."""
    # handle None, "", 0
    if not s:
        return None
    try:
        f = float(s)
        i = int(f)
        return i if f == i else f
    except ValueError:
        return s
