import re

import numpy as np

import lib.libhelperfunctions as hf
import lib.errors as err
import matplotlib.pyplot as plt

def import_cnc(fname):
    with open(fname) as f:
        text = f.read()

    return text


def clear_code(s):
    # replace all linebreaks
    lines = s.splitlines()
    # replace all indentations
    # divide lines by ';' and just take left side (ignores comments)
    lines = [li.strip().split(';')[0] for li in lines]
    return lines


def find_desired_section(textlist,
                         start_string='START_EBH:'.lower(),
                         end_string=None):
    textlist = hf.list_to_lower(textlist)
    if not end_string:
        end_string = ['END_EBH:'.lower(), 'RET'.lower()]
    try:
        start_idx = textlist.index(start_string)
    except ValueError:
        start_idx = None

    if start_idx is not None:
        for i, es in enumerate(end_string):
            try:
                end_idx = textlist.index(es, start_idx)
                break
            except ValueError:
                if i < len(end_string) - 1:
                    continue
                else:
                    end_idx = None
    else:
        end_idx = None

    return start_idx, end_idx


def get_parameter_mode(cnc_list, crit='if _paket'):
    converted_list = hf.list_to_lower(cnc_list)
    if any(crit in s for s in converted_list):
        mode = 'dual'
    else:
        mode = 'single'
    return mode


def get_correct_part(np):
    if np == 'NP-1':
        n_search = 'if _paket == "NP2"'.lower()
    elif np == 'NP-2':
        n_search = 'if _paket == "NP1"'.lower()
    else:
        raise AttributeError(f"Bauteil {np} unbekannt.")
    return n_search


def get_parameters(cnc, start_idx=None, end_idx=None, mode='single', n_p='NP-1', ax_finder=None, comment=';'):
    if not ax_finder:
        ax_dict = {'a': {
            'r': r'\ba{1}=\S+',
            'val': []
        },
            'sq': {
                'r': r'\bsq\s+\S*',
                'val': []
            },
            'sl': {
                'r': r'\bsl\s+\S*',
                'val': []
            },
            'fms': {
                'r': r'\bfms\s+\S*',
                'val': []
            },
            'soy': {
                'r': r'\bsoy\S+',
                'val': []
            },
            'g': {
                'r': r'g90|g91',
                'val': []
            }
        }
    else:
        ax_dict = ax_finder

    if start_idx is not None and end_idx is not None:
        section = cnc[start_idx:end_idx]
    else:
        section = cnc

    conv_data = hf.list_to_lower(section)

    exp = r'|'.join([v['r'] for k, v in ax_dict.items()])

    if mode == 'dual':
        # bestimme, welcher Abschnitt gescannt werden soll
        n_search = get_correct_part(n_p)
        scan_start, scan_end = find_desired_section(conv_data, start_string=n_search, end_string=['ENDIF'.lower()])
        erg = [e for e in (re.findall(exp, c) for i, c in enumerate(conv_data) if not scan_start <= i <= scan_end) if e]
    else:
        erg = [e for e in (re.findall(exp, c) for c in conv_data) if e]

    for k in ax_dict.keys():
        ax_dict[k]['val'] = [''] * len(erg)
        for i, stringlist in enumerate(erg):
            for s in stringlist:
                if re.match(ax_dict[k]['r'], s):
                    ax_dict[k]['val'][i] = re.sub(f'^{k}[= ]', '', s)

    return {k: v['val'] for k, v in ax_dict.items()}


def get_unknown_vars(c_list):
    flattend = hf.flatten(c_list)
    reg_vars = r'\b_.*?\b'
    erg = [e for e in (re.findall(reg_vars, s) for s in flattend) if e]
    return hf.remove_duplicates(hf.flatten(erg))


def evaluate_pb_expression(s):
    pat = r'([IiAa][Cc]\(|\))'
    return eval(re.sub(pat, '', s))


def gcode_to_values(code_dict, lead_axis='a', g_start='g91', inc=5.0, offset=True, force_fill=False):
    def get_distance(start, gs, val):
        if not val:
            return 0
        calc_val = evaluate_pb_expression(val)
        # Wenn Absolutwerte angenommen werden sollen
        if (')' in val and '(' not in val) or re.search(r'[AaCc]\(', val) or (gs == 'g90'):
            dist = calc_val - start
        elif gs == 'g91' or re.search(r'[IiCc]\(', val):
            dist = calc_val
        else:
            raise TypeError(f'Expression {val} cannot be evaluated.')

        return dist

    # wenn im dictionary keine G-Saetze enthalten sind
    cd = code_dict
    if 'g' not in cd.keys() or not cd['g']:
        raise AttributeError('No G-sets defined!')

    if lead_axis not in cd.keys():
        raise AttributeError('Leading Axis not properly defined')

    starts = {k: 0 for k in cd.keys()}
    data = {k: [] for k in cd.keys() if k != 'g'}
    lead_start = 0
    g_act = g_start
    steps = []
    for i in range(len(cd['g'])):
        # setze den aktuellen G-Befehl
        if cd['g'][i]:
            g_act = cd['g'][i]
        # ansonsten fülle die G-Befehle auf
        else:
            cd['g'][i] = g_act
        # überspringe Zeilen, in denen keine Bewegung der Führungsachse stattfindet
        if not cd[lead_axis][i]:
            steps.append(None)
            continue
        # Wenn noch keine Bewegung der Achse stattgefunden hat
        elif lead_start == 0:
            if offset:
                #  setze den Offsetwert als Startwert
                lead_start = hf.maybeMakeNumber(cd[lead_axis][i])
                continue

        lead_dist = get_distance(lead_start, g_act, cd[lead_axis][i])
        steps.append(abs(int(lead_dist/inc)))
        lead_start += lead_dist

    sorted_steps = [s for s in steps if s]
    for s in sorted_steps:
        if 0 <= s < 1:
            raise err.ValueTooLargeError(f'Increment {inc} is too coarse.')
        elif 1 <= s < 3 and not force_fill:
            raise err.ValueNearlyTooLargeError(f'Increment {inc} could be too coarse.')
        elif s > 1000 and not force_fill:
            raise err.ValueTooSmallError(f'Increment {inc} could be too small.')

    j = 0
    for i in range(len(cd[lead_axis])):
        s = steps[j]
        if not cd[lead_axis][i]:
            continue
        for k in (k for k in cd.keys() if k != 'g'):
            v = cd[k][i]
            if not s and v:
                starts[k] = hf.maybeMakeNumber(v)
            elif not s and not v:
                continue
            else:
                if i == len(cd[lead_axis]) - 1:
                    end_switch = True
                    add = 1
                else:
                    end_switch = False
                    add = 0

                start_val = starts[k]
                if k == 'fms' or k == 'f':
                    if not v:
                        stop_val = start_val
                    else:
                        stop_val = eval(v)
                    vals = np.repeat(stop_val, s+1)
                else:
                    g = cd['g'][i]
                    stop_val = start_val + get_distance(start_val, g, v)
                    vals = np.linspace(start_val, stop_val, num=s+add, endpoint=end_switch)
                if v:
                    starts[k] = stop_val
                data[k].append(vals)
        j += 1

    for k in data.keys():
        data[k] = hf.flatten(data[k])

    return data


def replace_missing_values(input_dict, replace_dict):
    def replace_with_dict(li, r_dict):
        list_to_string = ''.join(li)
        newlist = li.copy()
        for i, el in enumerate(li):
            for key, value in r_dict.items():
                if key in list_to_string and key in el:
                    newlist[i] = el.replace(key, str(value))
        return newlist

    outdict = {key: replace_with_dict(input_dict[key], replace_dict) for key in input_dict.keys()}

    return outdict


def parse_settings(c_list):
    reg_calcs = r'\(.*?\)'
    reg_vars = r'\b_.*?\b'
    return


def get_values_from_parameters(code, pars, mode='single', p_start=None, p_end=None, n_p='NP-1'):
    def get_value(t, search):
        pattern = fr'{search}\s.*?='
        prog = re.compile(pattern)

        for s in t:
            if prog.search(s) and '=' in s:
                result = s.split(';')[0].split('=')[1].strip()
                break
            else:
                result = []

        # result = [s.split(';')[0].split('=')[1].strip() for s in t if '=' in s if prog.match(s)]

        return result

    v_dict = {i: None for i in pars}

    code = hf.list_to_lower(code)

    if mode == 'single':
        for k in v_dict.keys():
            v_dict[k] = get_value(code, k)

        par_pat = r'_\w*'
        erg = [re.match(par_pat, v_dict[k]) for k in v_dict.keys()]
        while any(erg):
            for k in v_dict.keys():
                v_dict[k] = get_value(code, k)

            erg = [re.match(par_pat, v_dict[k]) for k in v_dict.keys()]
    elif mode == 'dual':
        para_data = code[p_start:p_end]
        # bestimme, welcher Abschnitt gescannt werden soll
        n_search = get_correct_part(n_p)
        scan_start, scan_end = find_desired_section(para_data, start_string=n_search, end_string=['ENDIF'.lower()])
        par_definition = [el for i, el in enumerate(para_data) if not scan_start <= i <= scan_end]
        for k in v_dict.keys():
            v_dict[k] = get_value(par_definition, k)
            if not v_dict[k]:
                v_dict[k] = get_value(code, k)
        par_pat = r'_\w*'
        erg = [re.search(par_pat, v_dict[k]) for k in v_dict.keys()]
        while any(erg):
            for k in v_dict.keys():
                match = re.findall(par_pat, v_dict[k])
                if not match:
                    continue
                old_val = match
                find_vals = [get_value(code, ov) for ov in old_val]
                if not all(find_vals):
                    print(f'Kann >>{old_val}<< nicht finden')
                    erg = False
                    break
                for old, new in zip(old_val, find_vals):
                    v_dict[k] = v_dict[k].replace(old, new)
            if not erg:
                break
            else:
                erg = [re.search(par_pat, v_dict[k]) for k in v_dict.keys()]

    for k in v_dict.keys():
        try:
            v_dict[k] = eval(v_dict[k])
        except ValueError:
            continue

    return v_dict


def print_data(d: dict):
    fig, ax = plt.subplots()
    for k in d.keys():
        ax.plot(d[k], label=k)

    plt.legend()
    plt.show()


def detect_offset(pars: dict, ax: str):
    for i, el in enumerate(pars.get(ax)):
        if el:
            row = i
            break
    offset = any([k for k in pars.keys() if k not in ['fms', 'g']])

    return offset


if __name__ == "__main__":
    filename = "../data/EBH_347_BS.MPF"
    nst = 'NP-1'
    leading_axis = 'a'
    increment = 0.25
    force_calc = False

    # importiere die Datei
    raw_cnc = import_cnc(filename)

    # bearbeite den CNC-Code
    cnc = clear_code(raw_cnc)

    # finde die Parameter
    strt, end = find_desired_section(cnc)
    ebh_cnc = cnc[strt:end]

    c_strt, c_end = find_desired_section(ebh_cnc, start_string='PYR_STRT'.lower(), end_string=['PYR_STOP'.lower()])

    contour_cnc = cnc[strt + c_strt:strt + c_end]
    contour_mode = get_parameter_mode(contour_cnc)

    contour_parameters = get_parameters(contour_cnc, mode=contour_mode, n_p=nst)

    # untersuche die Parameter auf Variablen
    par_cnc = cnc[strt:strt + c_strt]
    par_mode = get_parameter_mode(par_cnc)

    unknown_vars = get_unknown_vars(contour_parameters.values())

    if '_' + leading_axis + '_off' in unknown_vars:
        lead_offset = True
    else:
        lead_offset = False

    values = get_values_from_parameters(cnc, unknown_vars, p_start=strt, p_end=strt + c_strt, mode=par_mode)

    corrected_values = replace_missing_values(contour_parameters, values)

    # erzeuge aus der Tabelle Messwerte
    while True:
        try:
            gcode = gcode_to_values(corrected_values, inc=increment, offset=lead_offset, force_fill=force_calc)
            break
        except err.ValueTooLargeError as E:
            force_calc = False
            print(E)
            new_inc = float(input("Provide a new increment!\n"))
            increment = new_inc
        except (err.ValueNearlyTooLargeError, err.ValueTooSmallError) as E:
            force_calc = False
            print(E)
            while True:
                response = str(input("Continue anyway? (Y/N)\n"))
                if response in 'YyNnJj':
                    if response in 'YyJj':
                        force_calc = True
                        break
                    else:
                        new_inc = float(input("Provide a new increment!\n"))
                        increment = new_inc
                        break
                else:
                    print('Unsupported Answer.')

    print_data(gcode)


