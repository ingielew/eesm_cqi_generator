import sqlalchemy
from eff_snr import constants
from pandas import read_sql_query, DataFrame
from numpy import NaN
# from eff_snr.config.config import RESULTS_DIR
from os import path
from . import constants as data_constants
import eff_snr.config.config

def write_gen_data_to_df(bw, lambdas, pathloss_exp, punctured_sc, subband_eff_snr_arr, target_snr, wb_snr,
                         mean_cqi, eff_wb_cqi, eff_sb_cqi_arr):
    df_gen_new = DataFrame.from_dict(data_constants.generated_df)
    df_gen_new['lambdas'] = [lambdas]
    df_gen_new['pathloss_exp'] = [pathloss_exp]
    df_gen_new['target_snr'] = [target_snr]
    df_gen_new['bw'] = [bw]
    df_gen_new['punctured_sc'] = [punctured_sc]
    df_gen_new['cqi_est'] = [mean_cqi]
    df_gen_new['wb_eff_snr'] = [wb_snr]
    df_gen_new['wb_eff_cqi'] = [eff_wb_cqi]
    for i in range(0, constants.max_subbands):
        if i < len(subband_eff_snr_arr):
            df_gen_new['sb_{}_eff_snr'.format(i)] = subband_eff_snr_arr[i]
        else:
            df_gen_new['sb_{}_eff_snr'.format(i)] = 0

    for i in range(0, constants.max_subbands):
        if i < len(eff_sb_cqi_arr):
            df_gen_new['sb_{}_eff_cqi'.format(i)] = eff_sb_cqi_arr[i]
        else:
            df_gen_new['sb_{}_eff_cqi'.format(i)] = [NaN]

    return df_gen_new

    # self.df_gen = self.df_gen.append(df_gen_new, ignore_index=True)


def commit_gen_data_to_sql(df, engine):
    df.to_sql('data_input', con=engine, schema=None, if_exists='append', index=False, index_label=None)

def create_db_engine():
    db_path = path.join(eff_snr.config.config.RESULTS_DIR, 'data.db')
    print(db_path)
    return sqlalchemy.create_engine('{}:///{}'.format('sqlite', db_path))


class DatabaseHelper:
    def __init__(self):
        self.df_gen = DataFrame.from_dict(constants.generated_df)

    def read_data_from_db(self, eff_snr_cols, bw, target_snr, punctured_sc):
        if eff_snr_cols == 'all_sb':
            sql = 'SELECT {} ' \
                  'FROM data_input ' \
                  'WHERE "target_snr"={} AND "bw"={} AND "punctured_sc"={}' \
                .format(constants.all_eff_snr_columns, target_snr, bw, punctured_sc)
            return read_sql_query(sql, self.engine)
        elif eff_snr_cols == 'wb':
            sql = 'SELECT {} ' \
                  'FROM data_input ' \
                  'WHERE "target_snr"={} AND "bw"={} AND "punctured_sc"={}' \
                .format('wb_snr', target_snr, bw, punctured_sc)
            return read_sql_query(sql, self.engine), 1
        elif eff_snr_cols == 'all':
            sql = 'SELECT * ' \
                  'FROM data_input ' \
                  'WHERE "target_snr"={} AND "bw"={} AND "punctured_sc"={}' \
                .format(target_snr, bw, punctured_sc)
            return read_sql_query(sql, self.engine)

    def commit_result_data_to_sql(self, df_resource, table_name='data_result'):
        df_resource.to_sql(table_name, con=self.engine, schema=None, if_exists='append', index=False, index_label=None)

    engine = None
    df_gen = None
