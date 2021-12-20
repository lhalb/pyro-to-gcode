import re

def import_cnc(fname):
    with open(fname) as f:
        text = f.read()

    return text


def clear_code(s):
    # replace all linebreaks
    lines = s.splitlines()
    # replace all indentations
    lines = [l.lstrip() for l in lines]
    return lines


def find_desired_section(textlist,
                         start_string='START_EBH:',
                         end_string=None):
    if not end_string:
        end_string = ['END_EBH:', 'RET']
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
    converted_list = [s.lower() for s in cnc_list]
    if any(crit in s for s in converted_list):
        mode = 'dual'
    else:
        mode = 'single'
    return mode


def get_parameters(cnc,
                   p_s, p_e, c_s, c_e, p_m, c_m, ax_finder=None):
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

    contour = [s.lower() for s in cnc[c_s:c_e]]
    exp = r'|'.join([v['r'] for k, v in ax_dict.items()])
    erg = [e for e in (re.findall(exp, c) for c in contour) if e]

    for k in ax_dict.keys():
        ax_dict[k]['val'] = [0] * len(erg)
        for i, stringlist in enumerate(erg):
            for s in stringlist:
                if re.match(ax_dict[k]['r'], s):
                    ax_dict[k]['val'][i] = re.sub(f'^{k}[= ]', '', s)

    print(ax_dict)




if __name__ == "__main__":
    filename = "../data/EBH_347_BS.MPF"

    raw_cnc = import_cnc(filename)
    cnc = clear_code(raw_cnc)

    strt, end = find_desired_section(cnc)
    ebh_cnc = cnc[strt:end]

    c_strt, c_end = find_desired_section(ebh_cnc, start_string='PYR_STRT', end_string=['PYR_STOP'])

    par_cnc = cnc[strt:strt+c_strt]
    par_mode = get_parameter_mode(par_cnc)

    contour_cnc = cnc[strt+c_strt:strt+c_end]
    contour_mode = get_parameter_mode(contour_cnc)

    get_parameters(cnc, strt, strt+c_strt, strt+c_strt, strt+c_end, par_mode, contour_mode)






