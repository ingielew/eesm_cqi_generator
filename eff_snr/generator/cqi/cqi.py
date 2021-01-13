import numpy as np
from eff_snr import constants


def get_cqi_est(mean_snr):
    cqi = '0'
    for cqi_snr_thresh in constants.cqi_to_sinr_thresholds.keys():
        lin_snr_thresh = np.power(10, constants.cqi_to_sinr_thresholds[cqi_snr_thresh] / 10)
        if lin_snr_thresh < mean_snr:
            cqi = cqi_snr_thresh
    return cqi
