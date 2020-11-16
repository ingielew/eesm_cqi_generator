import numpy as np
import constants


def generate_complex_gaussian_distribution(n, mean_val, std_dev):
    return np.random.normal(loc=mean_val, scale=std_dev, size=(n, 2)).view(np.complex)


def generate_siso_channel_distribution(mean_val, std_dev, bw, pathloss_exp=2, distance=100):
    complex_normal_channel_gain = np.sqrt(1 / np.power(distance, pathloss_exp)) * \
                                  generate_complex_gaussian_distribution(
                                      constants.no_of_sc_in_prb * constants.no_of_prbs_in_cell_for_bw[bw],
                                      mean_val, std_dev
                                  )
    attenuation_per_sc = np.abs(complex_normal_channel_gain)  # Rayleigh-distributed attenuation
    # Chi-Squared distributed SNR
    pwr_channel_response = np.power(attenuation_per_sc, 2) / np.var(complex_normal_channel_gain)
    return pwr_channel_response


def puncture(input_arr, punctured_scs):
    for i in range(len(input_arr)-punctured_scs, len(input_arr)):
        input_arr[i] = 0
    return input_arr

# SIMO Scenario, based on:
# EESM-Based Link Adaptation in Point-to-Point Multi-Cell OFDM Systems: Modelling and Analysis
# J. Francis, N. B. Mehta


def mrc(tx_1_sc_rx_arr, tx_2_sc_rx_arr):
    combined = sum(np.power(abs(tx_1_sc_rx_arr), 2), np.power(abs(tx_2_sc_rx_arr), 2))
    return combined/np.var(sum(tx_1_sc_rx_arr, tx_2_sc_rx_arr))


def generate_simo_channel_distribution(mean_val, std_dev, bw, pathloss_exp=2, distance=100):
    ant_1_sc = np.sqrt(1 / np.power(distance, pathloss_exp)) * \
               generate_complex_gaussian_distribution(
                   constants.no_of_sc_in_prb * constants.no_of_prbs_in_cell_for_bw[bw], mean_val, std_dev)
    ant_2_sc = np.sqrt(1 / np.power(distance, pathloss_exp)) * \
               generate_complex_gaussian_distribution(
                   constants.no_of_sc_in_prb * constants.no_of_prbs_in_cell_for_bw[bw], mean_val, std_dev)
    return mrc(ant_1_sc, ant_2_sc)
