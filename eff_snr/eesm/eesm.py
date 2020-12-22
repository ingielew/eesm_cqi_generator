from eff_snr import constants
import numpy as np


def calc_eff_subband_snr(sc_snr_arr, param_lambda, cell_bw='20'):
    n_sbs = constants.no_of_subbands_for_bw[cell_bw]
    n_prbs_in_sb = constants.no_of_prbs_in_subband_for_bw[cell_bw]
    n_scs_in_sb = constants.no_of_sc_in_prb * n_prbs_in_sb
    negative_lambda_inverted = float(-1/param_lambda)
    subband_snr = []

    for sc in range(0, len(sc_snr_arr)):
        sc_snr_arr[sc] *= negative_lambda_inverted

    for sb in range(0, n_sbs):
        if sb*n_scs_in_sb+n_scs_in_sb < len(sc_snr_arr):
            subband_snr.extend(-1 * param_lambda * np.log(
                (1/n_scs_in_sb) * sum(np.exp(sc_snr_arr[sb*n_scs_in_sb:sb*n_scs_in_sb+n_scs_in_sb])))
            )
        else:
            n_scs_in_last_sb = len(sc_snr_arr) - sb*n_scs_in_sb
            subband_snr.extend(-1 * param_lambda * np.log(
                (1/n_scs_in_last_sb) * sum(np.exp(sc_snr_arr[sb*n_scs_in_sb:len(sc_snr_arr)])))
            )
    return subband_snr


def calc_eff_wb_snr(subband_snr_arr, param_lambda):
    negative_lambda_inverted = float(-1/param_lambda)

    for i in range(0, len(subband_snr_arr)):
        subband_snr_arr[int(i)] *= negative_lambda_inverted

    return -1*param_lambda*np.log((1/len(subband_snr_arr))*sum(np.exp(subband_snr_arr)))



