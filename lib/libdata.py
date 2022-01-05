import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

    # konvertiere die Datumsspalte zu Nanosekunden
    df['Zeit'] = pd.to_timedelta(df['Zeit']).dt.total_seconds()

    return df


def reset_timescale(data):
    t0 = data[0]
    timespan = data - t0
    return timespan


def plot_data(d, ib=None, cnc=None, filt=None):
    fig, ax = plt.subplots()
    x = d['Zeit'] * 10e-9
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
