from numpy import NaN, log10, float_power, power
from math import ceil


snr_range_min = -11
snr_range_max = 21
no_of_sc_in_prb = 12
max_subbands = 13
min_snr = -9  # lowest SNR yielding proper analytical output
max_snr = 23

sc_freq = 15000  # Hz
num_repetitions = 5000

supported_bandwidths = ['5', '10', '15', '20']

no_of_subbands_for_bw = {
    "5": 7,
    "10": 9,
    "15": 10,
    "20": 13
}

no_of_prbs_in_subband_for_bw = {
    "5": 4,
    "10": 6,
    "15": 8,
    "20": 8
}

avail_sb_ranges_per_bw = {
    '5': 7,
    '10': 9,
    '15': 10,
    '20': 13
}

no_of_prbs_in_cell_for_bw = {
    "5": 25,
    "10": 50,
    "15": 75,
    "20": 100
}

no_prbs_in_rgb_for_bw = {
    "5": 2,
    "10": 3,
    "15": 4,
    "20": 4
}

# Source:
# MCS Selection for Throughput Improvement in Downlink LTE Systems
#     J. Fan, Q. Yin, G. Y. Li, B. Peng, X. Zhu
cqi_to_lambda_values = {
    '0': 1,
    '1': 1,
    '2': 1.4,
    '3': 1.4,
    '4': 1.48,
    '5': 1.5,
    '6': 1.62,
    '7': 3.1,
    '8': 4.32,
    '9': 5.37,
    '10': 7.71,
    '11': 15.5,
    '12': 19.6,
    '13': 24.7,
    '14': 27.6,
    '15': 28,
}

# Source:
# MCS Selection for Throughput Improvement in Downlink LTE Systems
#     J. Fan, Q. Yin, G. Y. Li, B. Peng, X. Zhu
cqi_to_sinr_thresholds = {
    '0': NaN,
    '1': -9.478,
    '2': -6.658,
    '3': -4.098,
    '4': -1.798,
    '5': 0.399,
    '6': 2.424,
    '7': 4.489,
    '8': 6.367,
    '9': 8.456,
    '10': 10.266,
    '11': 12.218,
    '12': 14.122,
    '13': 15.849,
    '14': 17.786,
    '15': 19.809
}

# 1.4MHz and 3MHz cells skipped deliberately
data_ranges = {
    'pathloss_exp': [1, 2, 3, 4, 5, 6],
    'target_snr': [i for i in range(min_snr, max_snr, 2)],
    'bw': ['5', '10', '15', '20'],
    'punctured_sc_5Mhz': [12 * i * no_prbs_in_rgb_for_bw['5']
                          for i in range(0, ceil(no_of_prbs_in_cell_for_bw['5']/(no_prbs_in_rgb_for_bw['5']*2)))],
    'punctured_sc_10Mhz': [12 * i * no_prbs_in_rgb_for_bw['10']
                           for i in range(0, ceil(no_of_prbs_in_cell_for_bw['10']/(no_prbs_in_rgb_for_bw['10']*2)))],
    'punctured_sc_15Mhz': [12 * i * no_prbs_in_rgb_for_bw['15']
                           for i in range(0, ceil(no_of_prbs_in_cell_for_bw['15']/(no_prbs_in_rgb_for_bw['15']*2)))],
    'punctured_sc_20Mhz': [12 * i * no_prbs_in_rgb_for_bw['20']
                           for i in range(0, ceil(no_of_prbs_in_cell_for_bw['20']/(no_prbs_in_rgb_for_bw['20']*2)))]
}

noise_floor_db = 10*log10(1.38*float_power(10, -23)*290*1000) + 1.5 + 10*log10(sc_freq)
noise_floor_sc = power(10, noise_floor_db/10)


