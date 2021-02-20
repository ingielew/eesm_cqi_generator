from pandas import DataFrame

from eff_snr.data import database_helper
from eff_snr import constants as common_const
from eff_snr.data import constants as data_const

import os


class Parser:

    def __init__(self, db):
        self.db = db

    def handle_subband_results(self, bw, snr):
        results_df = DataFrame.from_dict(data_const.results_df)

def main(sim_config):
    results_filepath = sim_config['process_data_file']

    if results_filepath.endswith('csv'):
        return
    elif results_filepath.endswith('db'):
        db = database_helper.create_db_engine(os.path.normpath(results_filepath), is_db_existing=True)
        parser = Parser(db)

        for bw in sim_config['bw']:
            if str(bw) in common_const.data_ranges['bw']:
                for snr in common_const.data_ranges['target_snr']:
                    parser.handle_subband_results(bw, snr)
