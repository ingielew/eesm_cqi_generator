import numpy as np
import multiprocessing
from ast import literal_eval
from pandas import DataFrame
from . import constants
from copy import deepcopy
from .interf_noise_model import siso, puncture
from .cqi import cqi
from .eesm import eesm
from .data import database_helper


class EffSnrGenerator:
    def __init__(self, pathloss_exp, bw, target_snr, punctured_sc, distance):
        self.pathloss_exp = pathloss_exp
        self.bw = bw
        self.target_snr = target_snr
        self.punctured_sc = punctured_sc
        self.distance = distance

    def generate_eesm_distribution(self):
        mean = float(0)
        std_deviation = float(1 / np.sqrt(2))
        lin_target_snr = np.power(float(10), float(self.target_snr / 10))

        channel_gain_response = siso.generate_siso_channel_distribution(mean, std_deviation, self.bw,
                                                                                 pathloss_exp=self.pathloss_exp,
                                                                                 distance=self.distance)

        rx_snr_sc = channel_gain_response * lin_target_snr
        rx_snr_sc = puncture.puncture_higher(rx_snr_sc, self.punctured_sc)

        mean_snr = np.mean(rx_snr_sc)

        cqi_estimate = cqi.get_cqi_est(mean_snr)

        lambda_param = constants.cqi_to_lambda_values[cqi_estimate]

        subband_eff_snr_arr = eesm.calc_eff_subband_snr(sc_snr_arr=rx_snr_sc, param_lambda=lambda_param, cell_bw=self.bw)

        eff_sb_cqi = []
        for sb_eff_snr in subband_eff_snr_arr:
            eff_sb_cqi.append(cqi.get_cqi_est(sb_eff_snr))

        wb_snr = eesm.calc_eff_wb_snr(deepcopy(subband_eff_snr_arr), param_lambda=lambda_param)

        eff_wb_cqi = cqi.get_cqi_est(wb_snr)

        gen_df = database_helper.write_gen_data_to_df(self.bw,
                                                      lambda_param,
                                                      self.pathloss_exp,
                                                      self.punctured_sc,
                                                      subband_eff_snr_arr,
                                                      self.target_snr,
                                                      wb_snr, cqi_estimate, eff_wb_cqi, eff_sb_cqi)

        return gen_df


def run_generation(bw, distance, pathloss_exp, punctured_sc_perc, repetitions, target_snr):
    eff_snr_generator = EffSnrGenerator(pathloss_exp, bw, target_snr, punctured_sc_perc, distance)
    print('bw', bw, 'tar_snr', target_snr, 'rep', repetitions)
    df = DataFrame()
    for i in range(0, repetitions):
        df = df.append(eff_snr_generator.generate_eesm_distribution())

    return df


def main(sim_config):
    data_storage_type = sim_config['data_storage_type']
    print(data_storage_type)
    bw = list(literal_eval(sim_config['bw']))
    print(bw)
    target_snr = list(literal_eval(sim_config['target_snr']))
    # print(target_snr)

    punctured_sc_perc = literal_eval(sim_config['punctured_sc'])
    # print(punctured_sc_perc)
    puncturing_area = sim_config['puncturing_area']
    # print(puncturing_area)
    pathloss_exp = literal_eval(sim_config['pathloss_exp'])
    # print(pathloss_exp)
    distance = literal_eval(sim_config['distance'])
    # print(distance)
    repetitions = literal_eval(sim_config['repetitions'])
    # repetitions = 3
    # print(repetitions)

    db = None
    if data_storage_type == "sqlite3":
        db = database_helper.create_db_engine()

    is_multiproc = True

    if is_multiproc is True:
        input_list = []
        for bandwidths in bw:
            for tar_snr in target_snr:
                input_list.append((bandwidths, distance, pathloss_exp, punctured_sc_perc, repetitions, tar_snr))

        print(tuple(input_list))
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        gen_df = pool.starmap_async(run_generation, tuple(input_list))
        for data_frames in gen_df.get():
            database_helper.commit_gen_data_to_sql(data_frames, db)

    else:
        # for bandwidth in bw:
        # for tar_snr in target_snr:
        eff_snr_generator = EffSnrGenerator(pathloss_exp, bw, target_snr, punctured_sc_perc, distance)
        for i in range(0, repetitions):
            print('bw', bw, 'tar_snr', target_snr, 'rep', repetitions)
            # gen_df = eff_snr_generator.generate_eesm_distribution()
            # print(gen_df)
            # database_helper.commit_gen_data_to_sql(gen_df, db)


