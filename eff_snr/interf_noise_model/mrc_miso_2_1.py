from numpy import sqrt, power, var
from freq_attenuation import complex_gaussian
from eff_snr import constants


# MISO Scenario, based on:
# EESM-Based Link Adaptation in Point-to-Point Multi-Cell OFDM Systems: Modelling and Analysis
# J. Francis, N. B. Mehta
def _mrc(tx_1_sc_rx_arr, tx_2_sc_rx_arr):
    combined = sum(power(abs(tx_1_sc_rx_arr), 2), power(abs(tx_2_sc_rx_arr), 2))
    return combined/var(sum(tx_1_sc_rx_arr, tx_2_sc_rx_arr))


def generate_simo_channel_distribution(mean_val, std_dev, bw, pathloss_exp=2, distance=100):
    ant_1_sc = sqrt(1 / power(distance, pathloss_exp)) * \
               complex_gaussian.generate_complex_gaussian_distribution(
                   constants.no_of_sc_in_prb * constants.no_of_prbs_in_cell_for_bw[bw], mean_val, std_dev)
    ant_2_sc = sqrt(1 / power(distance, pathloss_exp)) * \
               complex_gaussian.generate_complex_gaussian_distribution(
                   constants.no_of_sc_in_prb * constants.no_of_prbs_in_cell_for_bw[bw], mean_val, std_dev)
    return _mrc(ant_1_sc, ant_2_sc)