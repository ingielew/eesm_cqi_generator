from numpy import sqrt, abs, power
from .freq_attenuation import complex_gaussian
from .. import constants


def generate_siso_channel_distribution(mean_val, std_dev, bw, pathloss_exp, distance):
    complex_normal_channel_gain = sqrt(1/power(float(distance), float(pathloss_exp))) * \
                                  complex_gaussian.generate_complex_gaussian_distribution(
                                      constants.no_of_sc_in_prb * constants.no_of_prbs_in_cell_for_bw[bw],
                                      mean_val, std_dev
                                  )
    attenuation_per_sc = abs(complex_normal_channel_gain)  # Rayleigh-distributed attenuation (var = ~0.2)
    # Chi-Squared distributed power response (var = 1)
    channel_ginr_response = power(attenuation_per_sc, 2)

    return channel_ginr_response