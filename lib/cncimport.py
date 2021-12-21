import re
import lib.libhelperfunctions as hf


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
                       'val': []}
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

    return [v['val'] for k, v in ax_dict.items()]


def get_unknown_vars(c_list):
    flattend = hf.flatten(c_list)
    reg_vars = r'\b_.*?\b'
    erg = [e for e in (re.findall(reg_vars, s) for s in flattend) if e]
    return hf.remove_duplicates(hf.flatten(erg))


def parse_settings(c_list):
    reg_calcs = r'\(.*?\)'
    reg_vars = r'\b_.*?\b'
    return


def get_values_from_parameters(code, pars, mode='single', p_start=None, p_end=None, n_p='NP-1'):
    def get_value(t, search):
        pattern = fr'{search}\s.*?='
        prog = re.compile(pattern)
        return [s.split(';')[0].split('=')[1].strip() for s in t if '=' in s if prog.match(s)]

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
        erg = [re.match(par_pat, v_dict[k]) for k in v_dict.keys()]
        while any(erg):
            for k in v_dict.keys():
                v_dict[k] = get_value(code, k)

            erg = [re.match(par_pat, v_dict[k]) for k in v_dict.keys()]

    return v_dict


if __name__ == "__main__":
    filename = "../data/EBH_347_BS.MPF"
    nst = 'NP-1'

    raw_cnc = import_cnc(filename)
    cnc = clear_code(raw_cnc)

    strt, end = find_desired_section(cnc)
    ebh_cnc = cnc[strt:end]

    c_strt, c_end = find_desired_section(ebh_cnc, start_string='PYR_STRT'.lower(), end_string=['PYR_STOP'.lower()])

    par_cnc = cnc[strt:strt+c_strt]
    par_mode = get_parameter_mode(par_cnc)

    contour_cnc = cnc[strt+c_strt:strt+c_end]
    contour_mode = get_parameter_mode(contour_cnc)

    contour_parameters = get_parameters(contour_cnc, mode=contour_mode, n_p=nst)

    unknown_vars = get_unknown_vars(contour_parameters)

    values = get_values_from_parameters(cnc, unknown_vars, p_start=strt, p_end=strt+c_strt, mode=par_mode)

    print(unknown_vars, values)







