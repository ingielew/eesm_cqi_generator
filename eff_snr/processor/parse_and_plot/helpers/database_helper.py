import sqlalchemy
from eff_snr import constants
from pandas import read_sql_query, DataFrame


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
