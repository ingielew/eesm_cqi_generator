import numpy as np
from . import constants
from copy import deepcopy
from .interf_noise_model import siso, puncture
from .cqi import cqi
from .eesm import eesm


class EffSnrGenerator:

    def __init__(self, db_engine=None):
        if db_engine is None:
            print('save')
        else:
            self.db = db_engine

    def generate_eesm_distribution(self, pathloss_exp, bw, target_snr, punctured_sc, distance=1):
        mean = float(0)
        std_deviation = float(1 / np.sqrt(2))
        lin_target_snr = np.power(float(10), float(target_snr / 10))
        channel_gain_response = []

        channel_gain_response = siso.generate_siso_channel_distribution(mean, std_deviation, bw,
                                                                                 pathloss_exp=pathloss_exp,
                                                                                 distance=distance)

        rx_snr_sc = channel_gain_response * lin_target_snr
        rx_snr_sc = puncture.puncture_higher(rx_snr_sc, punctured_sc)

        mean_snr = np.mean(rx_snr_sc)

        cqi_estimate = cqi.get_cqi_est(mean_snr)

        lambda_param = constants.cqi_to_lambda_values[cqi_estimate]

        subband_eff_snr_arr = eesm.calc_eff_subband_snr(sc_snr_arr=rx_snr_sc, param_lambda=lambda_param, cell_bw=bw)

        eff_sb_cqi = []
        for sb_eff_snr in subband_eff_snr_arr:
            eff_sb_cqi.append(cqi.get_cqi_est(sb_eff_snr))

        wb_snr = eesm.calc_eff_wb_snr(deepcopy(subband_eff_snr_arr), param_lambda=lambda_param)

        eff_wb_cqi = cqi.get_cqi_est(wb_snr)
        print(wb_snr)
        if self.db is not None:
            self.db.write_gen_data_to_df(bw, lambda_param, pathloss_exp, punctured_sc,
                                         subband_eff_snr_arr, target_snr, wb_snr, cqi_estimate, eff_wb_cqi, eff_sb_cqi)
        else:
            print("CSV")

    db = None