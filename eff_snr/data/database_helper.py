import sqlalchemy
from eff_snr import constants
from pandas import DataFrame
from numpy import NaN
from os import path
from . import constants as data_constants


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


def commit_gen_data_to_sql(df, engine):
    df.to_sql('data_input', con=engine, schema=None, if_exists='append', index=False, index_label=None)


def create_db_engine(write_path):
    db_path = path.join(write_path, 'data.db')
    print(db_path)
    return sqlalchemy.create_engine('{}:///{}'.format('sqlite', db_path))
