import numpy as np
import multiprocessing
from ast import literal_eval
from pandas import DataFrame
from . import constants
from copy import deepcopy
from eff_snr.generator.interf_noise_model import siso
from .generator.interf_noise_model import puncture
from .generator.cqi import cqi
from .generator.effective_sinr_mapping import eesm
from .data import database_helper
import eff_snr.config.common


class EffSnrGenerator:
    def __init__(self, pathloss_exp, bw, target_snr, punctured_sc, puncturing_area, distance):
        self.pathloss_exp = pathloss_exp
        self.bw = bw
        self.target_snr = target_snr
        self.punctured_sc = punctured_sc
        self.puncturing_area = puncturing_area
        self.distance = distance

    def generate_eesm_distribution(self):
        mean = float(0)
        std_deviation = float(1 / np.sqrt(2))
        lin_target_snr = np.power(float(10), float(self.target_snr / 10))

        channel_gain_response = siso.generate_siso_channel_distribution(mean, std_deviation, self.bw,
                                                                        pathloss_exp=self.pathloss_exp,
                                                                        distance=self.distance)

        rx_snr_sc = channel_gain_response * lin_target_snr
        rx_snr_sc, no_punctured_sc = puncture.puncture_sc(rx_snr_sc, self.punctured_sc, self.bw, self.puncturing_area)
        mean_snr = np.mean(rx_snr_sc)
        cqi_estimate = cqi.get_cqi_est(mean_snr)
        lambda_param = constants.cqi_to_lambda_values[cqi_estimate]
        subband_eff_snr_arr = eesm.calc_eff_subband_snr(sc_snr_arr=rx_snr_sc,
                                                        param_lambda=lambda_param, cell_bw=self.bw)

        eff_sb_cqi = []
        for sb_eff_snr in subband_eff_snr_arr:
            eff_sb_cqi.append(cqi.get_cqi_est(sb_eff_snr))

        wb_snr = eesm.calc_eff_wb_snr(deepcopy(subband_eff_snr_arr), param_lambda=lambda_param)

        eff_wb_cqi = cqi.get_cqi_est(wb_snr)

        gen_df = database_helper.write_gen_data_to_df(self.bw,
                                                      lambda_param,
                                                      self.pathloss_exp,
                                                      no_punctured_sc,
                                                      subband_eff_snr_arr,
                                                      self.target_snr,
                                                      wb_snr, cqi_estimate, eff_wb_cqi, eff_sb_cqi)
        return gen_df


def generate_eff_snr(bw, distance, pathloss_exp, punctured_sc_perc, puncturing_area, repetitions, target_snr):
    eff_snr_generator = EffSnrGenerator(pathloss_exp, bw, target_snr, punctured_sc_perc, puncturing_area, distance)
    print('bw', bw, 'tar_snr', target_snr, 'rep', repetitions)
    df = DataFrame()
    for i in range(0, repetitions):
        df = df.append(eff_snr_generator.generate_eesm_distribution())
    return df


def main(sim_config):
    data_storage_type = sim_config['data_storage_type']
    bw = list(literal_eval(sim_config['bw']))
    target_snr = list(literal_eval(sim_config['target_snr']))
    punctured_sc_perc = literal_eval(sim_config['punctured_sc'])
    puncturing_area = sim_config['puncturing_area']
    pathloss_exp = literal_eval(sim_config['pathloss_exp'])
    distance = literal_eval(sim_config['distance'])
    repetitions = literal_eval(sim_config['repetitions'])

    db = None
    results_path = eff_snr.config.common.RESULTS_DIR
    if data_storage_type == "sqlite3":
        db = database_helper.create_db_engine(results_path)

    is_multiprocessing = True

    if is_multiprocessing is True:
        input_list = []
        for bandwidths in bw:
            for tar_snr in target_snr:
                input_list.append((bandwidths, distance, pathloss_exp, punctured_sc_perc, puncturing_area, repetitions, tar_snr))

        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        gen_df_list = pool.starmap_async(generate_eff_snr, tuple(input_list))
        for data_frames in gen_df_list.get():
            if db is not None:
                database_helper.commit_gen_data_to_sql(data_frames, db)
            else:
                csv_filepath = eff_snr.config.common.join_paths(results_path, 'result.csv')
                data_frames.to_csv(csv_filepath, sep=',')
    else:
        for bandwidth in bw:
            for tar_snr in target_snr:
                eff_snr_generator = EffSnrGenerator(pathloss_exp, bandwidth, tar_snr, punctured_sc_perc, puncturing_area, distance)
                for i in range(0, repetitions):
                    gen_df = eff_snr_generator.generate_eesm_distribution()
                    if db is not None:
                        database_helper.commit_gen_data_to_sql(gen_df, db)
                    else:
                        csv_filepath = eff_snr.config.common.join_paths(results_path, 'result.csv')
                        gen_df.to_csv(csv_filepath, sep=',')
