from eff_snr.constants import data_ranges, no_of_prbs_in_cell_for_bw, no_of_sc_in_prb
from numpy import abs


def round_perc_sc_to_prb(perc_punctured_sc, bw):
    allowed_punctured_sc_values = list(data_ranges['punctured_sc_{}Mhz'.format(bw)])
    allowed_punctured_prb_values = [i/12 for i in allowed_punctured_sc_values]

    no_prbs_total = no_of_prbs_in_cell_for_bw['{}'.format(bw)]
    punctured_prbs = no_prbs_total*perc_punctured_sc/100

    closest_allowed_punctured_rb = max(allowed_punctured_prb_values)
    for allowed_punctured_prbs in allowed_punctured_prb_values:
        if abs(closest_allowed_punctured_rb - punctured_prbs) > abs(allowed_punctured_prbs - punctured_prbs):
            closest_allowed_punctured_rb = allowed_punctured_prbs

    return allowed_punctured_prb_values.index(closest_allowed_punctured_rb)*no_of_sc_in_prb


def puncture_sc(input_arr, perc_punctured_sc, bw, region="high"):
    no_punctured_res = round_perc_sc_to_prb(perc_punctured_sc, bw)

    if region == "higher":
        return puncture_higher(input_arr, no_punctured_res), no_punctured_res
    else:
        return puncture_lower(input_arr, no_punctured_res), no_punctured_res


def puncture_higher(input_arr, no_punctured_scs):
    for i in range(len(input_arr)-no_punctured_scs, len(input_arr)):
        input_arr[i] = 0
    return input_arr


def puncture_lower(input_arr, no_punctured_scs):
    for i in range(0, no_punctured_scs):
        input_arr[i] = 0
    return input_arr
