import sqlalchemy
import constants
from pandas import read_sql_query, DataFrame
from numpy import NaN


class Database:
    def __init__(self, database_type='sqlite', path='/data.db'):
        self.engine = sqlalchemy.create_engine('{}://{}'.format(database_type, path))
        self.df_gen = DataFrame.from_dict(constants.generated_df)

    def return_engine(self):
        return self.engine

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

    # def write_results_to_df(self, wb_mean, wb_mode, wb_var, sb_mean, sb_mode, sb_var, lambdas, pathloss_exp,
    #                          bw, punctured_sc, target_snr, sb_mean_delta=0, sb_mode_delta=0, wb_mean_delta=0,
    #                          wb_mode_delta=0):
    #     df = DataFrame.from_dict(constants.results_df)
    #     df['lambdas'] = [lambdas]
    #     df['pathloss_exp'] = [pathloss_exp]
    #     df['target_snr'] = [target_snr]
    #     df['bw'] = [bw]
    #     df['punctured_sc'] = [punctured_sc]
    #     df['wb_snr_mean'] = [wb_mean]
    #     df['wb_snr_mode'] = [wb_mode]
    #     df['wb_snr_mean_delta'] = [wb_mean_delta]
    #     df['wb_snr_mode_delta'] = [wb_mode_delta]
    #     df['wb_snr_var'] = [wb_var]
    #     df['sb_snr_mean'] = [sb_mean]
    #     df['sb_snr_mode'] = [sb_mode]
    #     df['sb_snr_mean_delta'] = [sb_mean_delta]
    #     df['sb_snr_mode_delta'] = [sb_mode_delta]
    #     df['sb_snr_var'] = [sb_var]
    #     df.to_sql('results', con=self.engine, schema=None, if_exists='append', index=True)

    def write_gen_data_to_df(self, bw, lambdas, pathloss_exp, punctured_sc, subband_eff_snr_arr, target_snr, wb_snr,
                             mean_cqi, eff_wb_cqi, eff_sb_cqi_arr):
        df_gen_new = DataFrame.from_dict(constants.generated_df)
        df_gen_new['lambdas'] = [lambdas]
        df_gen_new['pathloss_exp'] = [pathloss_exp]
        df_gen_new['target_snr'] = [target_snr]
        df_gen_new['bw'] = [bw]
        df_gen_new['punctured_sc'] = [punctured_sc]
        df_gen_new['cqi_est'] = mean_cqi
        df_gen_new['wb_eff_snr'] = wb_snr
        df_gen_new['wb_eff_cqi'] = eff_wb_cqi
        for i in range(0, constants.max_subbands):
            if i < len(subband_eff_snr_arr):
                df_gen_new['sb_{}_eff_snr'.format(i)] = subband_eff_snr_arr[i]
            else:
                df_gen_new['sb_{}_eff_snr'.format(i)] = NaN

        for i in range(0, constants.max_subbands):
            if i < len(eff_sb_cqi_arr):
                df_gen_new['sb_{}_eff_cqi'.format(i)] = eff_sb_cqi_arr[i]
            else:
                df_gen_new['sb_{}_eff_cqi'.format(i)] = NaN

        self.df_gen = self.df_gen.append(df_gen_new, ignore_index=True)

    def commit_gen_data_to_sql(self):
        self.df_gen.to_sql('data_input', con=self.engine, schema=None, if_exists='append', index=False, index_label=None)

    def commit_result_data_to_sql(self, df_resource):
        df_resource.to_sql('data_result', con=self.engine, schema=None, if_exists='append', index=False,
                           index_label=None)
    engine = None
    df_gen = None
