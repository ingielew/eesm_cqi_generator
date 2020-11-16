import constants
from copy import deepcopy
from scipy import stats
import numpy as np
from pandas import DataFrame
import plot_wrapper


class Parser:
    def __init__(self, database):
        self.db = database

    def handle_subband_results(self, bw, target_snr):
        results_df = DataFrame.from_dict(constants.results_df)

        combined_wb_dist_snr = []
        combined_wb_dist_cqi = []
        combined_sb_dist_snr = []
        combined_sb_dist_cqi = []
        combined_punctured_sc = []
        figure_name = "{}_{}_".format(bw, target_snr)

        for punctured_sc in constants.data_ranges['punctured_sc_{}Mhz'.format(bw)]:
            sc_figure_name = figure_name + "{}_".format(punctured_sc)
            if punctured_sc == 0:
                self.write_partial_df(results_df, 'deltas', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

            result = self.db.read_data_from_db('all', bw, target_snr, punctured_sc)
            self.write_partial_df(results_df, 'config', bw, target_snr, punctured_sc)

            sb_eff_snr_lin = []
            for i in range(0, constants.avail_sb_ranges_per_bw[bw]):
                sb_eff_snr_lin.extend(result['sb_{}_eff_snr'.format(i)])

            stripped_eff_snr_lin = []
            results_below_threshold = self.remove_invalid_values(sb_eff_snr_lin, stripped_eff_snr_lin)
            percentage_of_invalid_measurements = results_below_threshold/len(sb_eff_snr_lin)
            comment = "WB eff. SNR for BW={}, SNR={}, Punctured Subcarriers={},\n " \
                      "{} irrelevant results have been generated ({}%).\n" \
                    .format(bw, target_snr, punctured_sc, results_below_threshold, percentage_of_invalid_measurements)
            new_comment = self.snr_cqi_results_handle(results_df, 'sb_snr_lin', stripped_eff_snr_lin)
            sb_snr_lin_comment = comment + new_comment
            sb_snr_lin_fig_name = sc_figure_name + "sb_snr_lin"
            plot_wrapper.plot(stripped_eff_snr_lin, sb_snr_lin_comment, sb_snr_lin_fig_name, "SNR", "Occurrences")

            sb_eff_snr_db = 10*np.log10(stripped_eff_snr_lin)
            comment = "SB eff. SNR for BW={}, SNR={}, Punctured Subcarriers={},\n " \
                      "{} irrelevant results have been generated ({}%).\n" \
                    .format(bw, target_snr, punctured_sc, results_below_threshold, percentage_of_invalid_measurements)
            new_comment = self.snr_cqi_results_handle(results_df, 'sb_snr_db', sb_eff_snr_db)
            sb_snr_lin_comment = comment + new_comment

            sb_snr_db_fig_name = sc_figure_name + "sb_snr_db"
            plot_wrapper.plot(sb_eff_snr_db, sb_snr_lin_comment, sb_snr_db_fig_name, "SNR", "Occurrences")

            sb_eff_cqi = []
            for i in range(0, constants.avail_sb_ranges_per_bw[bw]):
                sb_eff_cqi.extend(result['sb_{}_eff_cqi'.format(i)])
            stripped_sb_eff_cqi = []
            self.remove_invalid_values(sb_eff_cqi, stripped_sb_eff_cqi)
            sb_eff_cqi = [int(elem) for elem in stripped_sb_eff_cqi]

            comment = "SB CQI dist. For BW={}, SNR={}, Punctured Subcarriers={}.\n".format(bw, target_snr, punctured_sc)
            new_comment = self.snr_cqi_results_handle(results_df, 'sb_cqi', sb_eff_cqi)
            sb_cqi_comment = comment + new_comment
            sb_cqi_fig_name = sc_figure_name + "sb_cqi"
            plot_wrapper.plot(sb_eff_cqi, sb_cqi_comment, sb_cqi_fig_name, "CQI", "Occurrences")

            wb_eff_snr_lin = result['wb_eff_snr']
            stripped_wb_eff_snr_lin = []
            results_below_threshold = self.remove_invalid_values(wb_eff_snr_lin, stripped_wb_eff_snr_lin)
            percentage_of_invalid_measurements = results_below_threshold/len(wb_eff_snr_lin)
            comment = "WB eff. SNR for BW={}, SNR={}, Punctured Subcarriers={},\n" \
                      " {} irrelevant results have been generated ({}%).\n" \
                    .format(bw, target_snr, punctured_sc, results_below_threshold, percentage_of_invalid_measurements)
            new_comment = self.snr_cqi_results_handle(results_df, 'wb_snr_lin', wb_eff_snr_lin)
            wb_snr_lin_comment = comment + new_comment
            wb_snr_lin_fig_name = sc_figure_name + "wb_snr_lin"
            plot_wrapper.plot(stripped_eff_snr_lin, wb_snr_lin_comment, wb_snr_lin_fig_name, "SNR", "Occurrences")

            wb_eff_snr_db = 10*np.log10(stripped_wb_eff_snr_lin)
            comment = "WB eff. SNR for BW={}, SNR={}, Punctured Subcarriers={},\n" \
                      " {} irrelevant results have been generated ({}%).\n" \
                    .format(bw, target_snr, punctured_sc, results_below_threshold, percentage_of_invalid_measurements)
            new_comment = self.snr_cqi_results_handle(results_df, 'wb_snr_db', wb_eff_snr_db)
            wb_snr_db_comment = comment + new_comment
            wb_snr_db_fig_name = sc_figure_name + "wb_snr_db"
            plot_wrapper.plot(wb_eff_snr_db, wb_snr_db_comment, wb_snr_db_fig_name, "SNR", "Occurrences")

            wb_eff_cqi = result['wb_eff_cqi']
            wb_eff_cqi = [int(elem) for elem in wb_eff_cqi]
            comment = "WB CQI dist. For BW={}, SNR={}, Punctured Subcarriers={}.\n".format(bw, target_snr, punctured_sc)
            new_comment = self.snr_cqi_results_handle(results_df, 'wb_cqi', wb_eff_cqi)
            wb_cqi_comment = comment + new_comment
            wb_snr_db_fig_name = sc_figure_name + "wb_cqi"
            plot_wrapper.plot(wb_eff_cqi, wb_cqi_comment, wb_snr_db_fig_name, "CQI", "Occurrences")

            if punctured_sc > 0:
                self.calculate_deltas(results_df, sb_eff_cqi, sb_eff_snr_db, stripped_eff_snr_lin, wb_eff_cqi,
                                      wb_eff_snr_db,
                                      stripped_wb_eff_snr_lin)
            else:
                self.update_reference_data(sb_eff_cqi, sb_eff_snr_db, stripped_eff_snr_lin, wb_eff_cqi, wb_eff_snr_db,
                                           stripped_wb_eff_snr_lin)

            combined_wb_dist_snr.append(deepcopy(wb_eff_snr_db))
            combined_wb_dist_cqi.append(np.round(wb_eff_cqi))
            combined_sb_dist_snr.append(deepcopy(sb_eff_snr_db))
            combined_sb_dist_cqi.append(np.round(sb_eff_cqi))
            combined_punctured_sc.append(punctured_sc)
            self.db.commit_result_data_to_sql(results_df)

        comment = ""
        combined_wb_snr_figure_name = "combined_wb_snr_bw_{}_snr_{}".format(bw, target_snr)
        plot_wrapper.plot(combined_wb_dist_snr, comment, combined_wb_snr_figure_name, "SNR", "Occurrences")
        combined_wb_cqi_figure_name = "combined_wb_cqi_{}_snr_{}".format(bw, target_snr)
        plot_wrapper.plot(combined_wb_dist_cqi, comment, combined_wb_cqi_figure_name, "CQI", "Occurrences")
        combined_sb_snr_figure_name = "combined_sb_snr_{}_snr_{}".format(bw, target_snr)
        plot_wrapper.plot(combined_sb_dist_snr, comment, combined_sb_snr_figure_name, "SNR", "Occurrences")
        combined_sb_cqi_figure_name = "combined_sb_cqi_{}_snr_{}".format(bw, target_snr)
        plot_wrapper.plot(combined_sb_dist_cqi, comment, combined_sb_cqi_figure_name, "CQI", "Occurrences")

        scatter_combined_wb_name = "scatter_snr_{}_{}".format(bw, target_snr)
        plot_wrapper.scatter_plot(combined_punctured_sc, combined_wb_dist_snr, comment, scatter_combined_wb_name,
                                    'Punctured resources', 'SNR')

        self.clear_temp_variables()

    def calculate_deltas(self, results_df, sb_eff_cqi, sb_eff_snr_db, sb_eff_snr_lin, wb_eff_cqi, wb_eff_snr_db,
                         wb_eff_snr_lin):
        if sb_eff_cqi:
            sb_cqi_delta = abs(self.reference_sb_cqi_delta - np.round(np.mean(sb_eff_cqi), 2))
        else:
            sb_cqi_delta = None

        if wb_eff_snr_lin:
            wb_snr_mean_delta = abs(self.reference_wb_snr_mean_delta - np.mean(wb_eff_snr_lin))
            wb_snr_mode_delta = abs(self.reference_wb_snr_mode_delta - float(stats.mode(wb_eff_snr_lin)[0]))
        else:
            wb_snr_mean_delta = None
            wb_snr_mode_delta = None

        if any(wb_eff_snr_db):
            wb_snr_mean_delta_db = abs(abs(self.reference_wb_snr_mean_delta_db) - np.mean(wb_eff_snr_db))
            wb_snr_mode_delta_db = abs(self.reference_wb_snr_mode_delta_db - float(stats.mode(wb_eff_snr_db)[0]))
        else:
            wb_snr_mean_delta_db = None
            wb_snr_mode_delta_db = None

        if sb_eff_snr_lin:
            sb_snr_mean_delta = abs(self.reference_sb_snr_mean_delta - np.mean(sb_eff_snr_lin))
            sb_snr_mode_delta = abs(self.reference_sb_snr_mode_delta - float(stats.mode(sb_eff_snr_lin)[0]))
        else:
            sb_snr_mean_delta = None
            sb_snr_mode_delta = None

        if any(sb_eff_snr_db):
            sb_snr_mean_delta_db = abs(self.reference_sb_snr_mean_delta_db - np.mean(sb_eff_snr_db))
            sb_snr_mode_delta_db = abs(self.reference_sb_snr_mode_delta_db - float(stats.mode(sb_eff_snr_db)[0]))
        else:
            sb_snr_mean_delta_db = None
            sb_snr_mode_delta_db = None

        if wb_eff_cqi:
            wb_cqi_delta = abs(self.reference_wb_cqi_delta - np.round(np.mean(wb_eff_cqi), 2))
        else:
            wb_cqi_delta = None

        self.write_partial_df(results_df, 'deltas', wb_snr_mean_delta, wb_snr_mode_delta, wb_snr_mean_delta_db,
                              wb_snr_mode_delta_db, sb_snr_mean_delta, sb_snr_mode_delta, sb_snr_mean_delta_db,
                              sb_snr_mode_delta_db, wb_cqi_delta, sb_cqi_delta)

    def update_reference_data(self, eff_sb_cqi, sb_eff_snr_db, sb_eff_snr_lin, wb_eff_cqi, wb_eff_snr_db,
                              wb_eff_snr_lin):

        if wb_eff_cqi is not None:
            self.reference_wb_cqi_delta = np.round(np.mean(wb_eff_cqi), 2)
        else:
            self.reference_wb_cqi_delta = None

        if eff_sb_cqi is not None:
            self.reference_sb_cqi_delta = np.round(np.mean(eff_sb_cqi), 2)
        else:
            self.reference_sb_cqi_delta = None

        if wb_eff_snr_lin:
            self.reference_wb_snr_mean_delta = np.mean(wb_eff_snr_lin)
            self.reference_wb_snr_mode_delta = float(stats.mode(wb_eff_snr_lin)[0])
        else:
            self.reference_wb_snr_mean_delta = 0
            self.reference_wb_snr_mode_delta = 0

        if wb_eff_snr_db is not None:
            self.reference_wb_snr_mean_delta_db = np.mean(wb_eff_snr_db)
            self.reference_wb_snr_mode_delta_db = float(stats.mode(wb_eff_snr_db)[0])
        else:
            self.reference_wb_snr_mean_delta_db = -13
            self.reference_wb_snr_mode_delta_db = -13

        if sb_eff_snr_lin:
            self.reference_sb_snr_mean_delta = np.mean(sb_eff_snr_lin)
            self.reference_sb_snr_mode_delta = float(stats.mode(sb_eff_snr_lin)[0])
        else:
            self.reference_sb_snr_mean_delta = 0
            self.reference_sb_snr_mode_delta = 0
        if sb_eff_snr_db is not None:
            self.reference_sb_snr_mean_delta_db = np.mean(sb_eff_snr_db)
            self.reference_sb_snr_mode_delta_db = float(stats.mode(sb_eff_snr_db)[0])
        else:
            self.reference_sb_snr_mean_delta_db = -13
            self.reference_sb_snr_mode_delta_db = -13

    def clear_temp_variables(self):
        self.reference_wb_cqi_delta = 0
        self.reference_sb_cqi_delta = 0
        self.reference_wb_snr_mean_delta = 0
        self.reference_wb_snr_mode_delta = 0
        self.reference_wb_snr_mean_delta_db = 0
        self.reference_wb_snr_mode_delta_db = 0
        self.reference_sb_snr_mean_delta = 0
        self.reference_sb_snr_mode_delta = 0
        self.reference_sb_snr_mean_delta_db = 0
        self.reference_sb_snr_mode_delta_db = 0

    def remove_invalid_values(self, input_list, output_list):
        results_below_threshold = 0

        for index in input_list:
            if index is not None and index is not np.NaN:
                if float(index) > 0.0501:  # SNR smaller than -13 dB
                    output_list.append(index)
            else:
                results_below_threshold += 1
        return results_below_threshold

    def snr_cqi_results_handle(self, results_df, measurement_type, result):
        if any(result):
            if not measurement_type == 'sb_cqi' or measurement_type == 'wb_cqi':
                result = np.round(result, 3)
            unique = np.unique(result)
            if len(unique) > 1:
                nobs, min_max, mean, var, skew, kurt = stats.describe(result)
                mode, count = stats.mode(result)
                mean = round(mean, 4)
                mode = round(float(mode), 3)
                var = round(var, 4)
                comment = "$N={0}, \mu={1}, \sigma^{{2}}={2}, Mo={3}({4})$".format(nobs, mean, var, mode, count)
            else:
                mean = result[0]
                mode = result[0]
                var = 0
                comment = "$N={0}, \mu={1}, \sigma^{{2}}={2}"\
                    .format(len(result), result[0], 0)

            self.write_partial_df(results_df, measurement_type, mean, mode, var)
        else:
            comment = "No valid results for this configuration."

        return comment

    def write_partial_df(self, results_df, meas_input, *args):
        if meas_input == 'config':
            results_df['bw'] = [args[0]]
            results_df['target_snr'] = [args[1]]
            results_df['punctured_sc'] = [args[2]]

        if meas_input == 'wb_snr_lin':
            results_df['wb_snr_mean'] = [args[0]]
            results_df['wb_snr_mode'] = [args[1]]
            results_df['wb_snr_var'] = [args[2]]

        if meas_input == 'wb_snr_db':
            results_df['wb_snr_mean_db'] = [args[0]]
            results_df['wb_snr_mode_db'] = [args[1]]
            results_df['wb_snr_var_db'] = [args[2]]

        if meas_input == 'deltas':
            results_df['wb_snr_mean_delta'] = [args[0]]
            results_df['wb_snr_mode_delta'] = [args[1]]
            results_df['wb_snr_mean_delta_db'] = [args[2]]
            results_df['wb_snr_mode_delta_db'] = [args[3]]
            results_df['sb_snr_mean_delta'] = [args[4]]
            results_df['sb_snr_mode_delta'] = [args[5]]
            results_df['sb_snr_mean_delta_db'] = [args[6]]
            results_df['sb_snr_mode_delta_db'] = [args[7]]
            results_df['wb_cqi_delta'] = [args[8]]
            results_df['sb_cqi_delta'] = [args[9]]

        if meas_input == 'sb_snr_lin':
            results_df['sb_snr_mean'] = [args[0]]
            results_df['sb_snr_mode'] = [args[1]]
            results_df['sb_snr_var'] = [args[2]]

        if meas_input == 'sb_snr_db':
            results_df['sb_snr_mean_db'] = [args[0]]
            results_df['sb_snr_mode_db'] = [args[1]]
            results_df['sb_snr_var_db'] = [args[2]]

        if meas_input == 'wb_cqi':
            results_df['wb_cqi_mean'] = [args[0]]
            results_df['wb_cqi_mode'] = [args[1]]
            results_df['wb_cqi_delta'] = [args[2]]

        if meas_input == 'sb_cqi':
            results_df['sb_cqi_mean'] = [args[0]]
            results_df['sb_cqi_mode'] = [args[1]]
            results_df['sb_cqi_delta'] = [args[2]]

    db = None
    reference_wb_cqi_delta = 0
    reference_sb_cqi_delta = 0
    reference_wb_snr_mean_delta = 0
    reference_wb_snr_mode_delta = 0
    reference_wb_snr_mean_delta_db = 0
    reference_wb_snr_mode_delta_db = 0
    reference_sb_snr_mean_delta = 0
    reference_sb_snr_mode_delta = 0
    reference_sb_snr_mean_delta_db = 0
    reference_sb_snr_mode_delta_db = 0
