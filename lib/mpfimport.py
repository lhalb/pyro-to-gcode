import pandas as pd
import re
from libhelperfunctions import maybeMakeNumber


def split_axis_and_data(s: str) -> dict:
    list_data = s.split(' ')
    keys = list_data[0::2]
    data = [maybeMakeNumber(v) for v in list_data[1::2]]

    return {k: v for k, v in zip(keys, data)}


def import_spf(fname):
    header = ''
    data = {}
    with open(fname, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()

    for line in all_lines:
        if '=' not in line:
            continue
        # replace '=' with ' ' to seperate Axis from value
        line = line.rstrip().replace('=', ' ')
        # clear offsets and pro-beam syntax
        cleared_line = re.sub(r'\b_SL_OFF\b|\b_SQ_OFF\b|[()+]', '', line)
        split_line = split_axis_and_data(cleared_line)
        # create as many empty lists as keys for the first line
        if not header:
            for key in split_line:
                data[key] = []
            header = data.keys()
        # append values to list
        for key in split_line:
            data[key].append(split_line[key])

    dataframe = pd.DataFrame(data=data)

    return dataframe


if __name__ == '__main__':
    import os
    source = r'F:\PycharmProjects\pyro-to-gcode\data\nc_code'
    outdir = r'F:\PycharmProjects\pyro-to-gcode\export\nc_data'

    for file in os.listdir(source):
        name, ext = os.path.splitext(file)
        if ext == '.SPF':
            filename = os.path.join(source, file)

            # print('read from: ', filename)

            df = import_spf(filename)

            outname = os.path.join(outdir, name)
            outname += '.xlsx'

            # print('Save to: ', outname)

            df.to_excel(outname)

    print('done')
