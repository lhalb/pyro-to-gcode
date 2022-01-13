import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, medfilt
pd.options.mode.chained_assignment = None
matplotlib.use('Qt5Agg')


def import_data(f, colnames=None):
    if not colnames:
        cn = ['Zeit', 'Temperatur', 'Sollwert', 'P-Ausgabe']
    else:
        cn = colnames
    # Spalten einen Datentyp zuweisen (erhoeht Geschwindigkeit)
    type_dict = {'Temperatur': np.float64, 'P-Ausgabe': np.float64}
    # CSV einlesen
    df = pd.read_csv(f, encoding='latin_1', header=0, sep=';', decimal=',',
                     usecols=cn, dtype=type_dict)

    df['Sollwert'] = pd.to_numeric(df['Sollwert'].str.replace(',', '.'), errors='coerce')
    # Verwirf die ungültigen Werte
    df.dropna(inplace=True)
    # setze den Index zurück, um Daten leichter handlen zu können
    df.reset_index(drop=True, inplace=True)
    df['RAW-Time'] = df['Zeit']
    # konvertiere die Datumsspalte zu Zeiteinheit
    df['Zeit'] = pd.to_timedelta(df['Zeit']).dt.total_seconds()
    # konvertiere Zeiteinheit, da Anzahl an Nachkommastellen variieren kann
    digits = get_digits_after_comma(df['RAW-Time'][0])
    if digits > 0:
        df['Zeit'] = df['Zeit'] * 10**-digits

    return df


def get_cnc_times(calc_data: pd.Series, num: int):
    min_val = calc_data.min()
    max_val = calc_data.max()
    return np.linspace(min_val, max_val, num)


def get_corresponding_powers(source_data: pd.DataFrame,
                             dest_data: pd.DataFrame,
                             comp_col: str = 'Zeit',
                             search_col: str = 'P-Ausgabe'):
    def get_index(df: pd.DataFrame, col: str, val: float):
        return df[col].sub(val).abs().idxmin()

    vals = len(dest_data.index)
    ret_data = [None] * vals
    for i in range(vals):
        search_val = dest_data[comp_col].iloc[i]
        found_idx = get_index(source_data, comp_col, search_val)
        ret_data[i] = source_data[search_col].iloc[found_idx]

    return ret_data


def apply_rolling_average(data: pd.Series, n):
    return data.rolling(n).mean()


def apply_median_filter(data, ks):
    return medfilt(data, ks)


def apply_savgol_filter(data, window, polyorder, deriv, delta, mode):
    return savgol_filter(data, polyorder=polyorder, window_length=window, deriv=deriv, delta=delta, mode=mode)


def get_digits_after_comma(string: str):
    if not ',' in string:
        return 0
    else:
        return len(string.split(',')[-1])


def reset_timescale(data: pd.Series):
    d = data.dropna()
    return d - d.iloc[0]


def export_data(path, sheets: list,  data: list):
    with pd.ExcelWriter(path) as writer:
        for d, sheetname in zip(data, sheets):
            d.to_excel(writer, sheet_name=sheetname)


def plot_data(d, ib=None, cnc=None, filt=None):
    fig, ax = plt.subplots()
    x = d['Zeit']
    y11 = d['Temperatur']
    y12 = d['Sollwert']

    ax.plot(x, y11, 'r-', label=y11.name)
    ax.plot(x, y12, 'k-', label=y12.name)

    lines, labels = ax.get_legend_handles_labels()

    testlist = [ib, cnc, filt]
    y2_list = []
    for i, t in enumerate(testlist):
        if t:
            y2_list.append(t)
        else:
            if i == 0:
                y2_list.append(d['P-Ausgabe'])

    if y2_list:
        ax2 = ax.twinx()
        for y2 in y2_list:
            ax2.plot(x, y2, label=y2.name)

        lines2, labels2 = ax2.get_legend_handles_labels()

        ax2.legend(lines + lines2, labels + labels2, loc=0)

    plt.show()


def export_data_to_gcode(path: str, data: pd.DataFrame, la: str):
    header = 'CONTOUR:\nG1 G91 G64'

    return
