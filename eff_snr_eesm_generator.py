import numpy as np
import constants
import channel_model
from copy import deepcopy
from sys import float_info


def eesm_sc_into_subband_snr(sc_snr_arr, param_lambda=10, cell_bw='20'):
    n_sbs = constants.no_of_subbands_for_bw[cell_bw]
    n_prbs_in_sb = constants.no_of_prbs_in_subband_for_bw[cell_bw]
    n_scs_in_sb = constants.no_of_sc_in_prb*n_prbs_in_sb

    subband_snr = np.empty([n_sbs, 1])

    negative_lambda_inverted = float(-1/param_lambda)

    for sc in range(0, len(sc_snr_arr)):
        sc_snr_arr[sc] *= negative_lambda_inverted

    for sb in range(0, n_sbs):
        if sb*n_scs_in_sb+n_scs_in_sb < len(sc_snr_arr):
            subband_snr[sb] = -1 * param_lambda * np.log(
                (1/n_scs_in_sb) * sum(np.exp(sc_snr_arr[sb*n_scs_in_sb:sb*n_scs_in_sb+n_scs_in_sb]))
            )
        else:
            n_scs_in_last_sb = len(sc_snr_arr) - sb*n_scs_in_sb
            subband_snr[sb] = -1 * param_lambda * np.log(
                (1/n_scs_in_last_sb) * sum(np.exp(sc_snr_arr[sb*n_scs_in_sb:len(sc_snr_arr)]))
            )
    return subband_snr


def eesm_into_wb_snr(subband_snr_arr, param_lambda=10):
    negative_lambda_inverted = float(-1/param_lambda)

    for i in range(0, len(subband_snr_arr)):
        subband_snr_arr[int(i)] *= negative_lambda_inverted

    return -1*param_lambda*np.log((1/len(subband_snr_arr))*sum(np.exp(subband_snr_arr)))


def get_cqi_est(mean_snr):
    cqi = '0'
    for cqi_snr_thresh in constants.cqi_to_sinr_thresholds.keys():
        lin_snr_thresh = np.power(10, constants.cqi_to_sinr_thresholds[cqi_snr_thresh]/10)
        if lin_snr_thresh < mean_snr:
            cqi = cqi_snr_thresh
    return cqi


class EffSnrEesmGenerator:
    def __init__(self, database):
        self.db = database

    def commit_results_to_db(self):
        self.db.commit_gen_data_to_sql()

    def generate_eesm_distribution(self, pathloss_exp, bw, target_snr, punctured_sc,
                                   distance=100, tx_scheme='siso'):

        mean = 0
        std_deviation = 1 / np.sqrt(2)
        lin_target_snr = np.power(10, (target_snr/10))
        pwr_channel_response = []
        if tx_scheme == 'siso':
            pwr_channel_response = channel_model.generate_siso_channel_distribution(mean, std_deviation, bw,
                                                                                    pathloss_exp=pathloss_exp,
                                                                                    distance=distance)
        elif tx_scheme == 'miso':
            pwr_channel_response = channel_model.generate_simo_channel_distribution(mean, std_deviation, bw,
                                                                                    pathloss_exp=pathloss_exp,
                                                                                    distance=distance)
        rx_snr_sc = pwr_channel_response*lin_target_snr
        rx_snr_sc = channel_model.puncture(rx_snr_sc, punctured_sc)+constants.noise_floor_sc

        mean_snr = 10*np.log10(np.mean(rx_snr_sc))

        cqi = get_cqi_est(mean_snr)
        lambda_param = constants.cqi_to_lambda_values[cqi]

        subband_eff_snr_arr = eesm_sc_into_subband_snr(sc_snr_arr=rx_snr_sc, param_lambda=lambda_param, cell_bw=bw)

        eff_sb_cqi = []
        for sb_eff_snr in subband_eff_snr_arr:
            subband_eff_snr_arr_db = 10*np.log10(sb_eff_snr)
            eff_sb_cqi.append(get_cqi_est(subband_eff_snr_arr_db))

        wb_snr = eesm_into_wb_snr(deepcopy(subband_eff_snr_arr), param_lambda=lambda_param)
        wb_snr_db = 10*np.log10(wb_snr)
        eff_wb_cqi = get_cqi_est(wb_snr_db)
        self.db.write_gen_data_to_df(bw, lambda_param, pathloss_exp, punctured_sc,
                                     subband_eff_snr_arr, target_snr, wb_snr, cqi, eff_wb_cqi, eff_sb_cqi)

    db = None
