generated_df = {
    'lambdas': [],
    'pathloss_exp': [],
    'target_snr': [],
    'bw': [],
    'punctured_sc': [],
    'cqi_est': [],
    'wb_eff_snr': [],
    'wb_eff_cqi': [],
    'sb_0_eff_snr': [],
    'sb_0_eff_cqi': [],
    'sb_1_eff_snr': [],
    'sb_1_eff_cqi': [],
    'sb_2_eff_snr': [],
    'sb_2_eff_cqi': [],
    'sb_3_eff_snr': [],
    'sb_3_eff_cqi': [],
    'sb_4_eff_snr': [],
    'sb_4_eff_cqi': [],
    'sb_5_eff_snr': [],
    'sb_5_eff_cqi': [],
    'sb_6_eff_snr': [],
    'sb_6_eff_cqi': [],
    'sb_7_eff_snr': [],
    'sb_7_eff_cqi': [],
    'sb_8_eff_snr': [],
    'sb_8_eff_cqi': [],
    'sb_9_eff_snr': [],
    'sb_9_eff_cqi': [],
    'sb_10_eff_snr': [],
    'sb_10_eff_cqi': [],
    'sb_11_eff_snr': [],
    'sb_11_eff_cqi': [],
    'sb_12_eff_snr': [],
    'sb_12_eff_cqi': []
}


results_df = {
    'bw': [],
    'target_snr': [],
    'punctured_sc': [],
    'wb_snr_mean': [],
    'wb_snr_mode': [],
    'wb_snr_mean_delta': [],
    'wb_snr_mode_delta': [],
    'wb_snr_var': [],
    'wb_snr_mean_db': [],
    'wb_snr_mode_db': [],
    'wb_snr_mean_delta_db': [],
    'wb_snr_mode_delta_db': [],
    'wb_snr_var_db': [],
    'sb_snr_mean': [],
    'sb_snr_mode': [],
    'sb_snr_mean_delta': [],
    'sb_snr_mode_delta': [],
    'sb_snr_var': [],
    'sb_snr_mean_db': [],
    'sb_snr_mode_db': [],
    'sb_snr_mean_delta_db': [],
    'sb_snr_mode_delta_db': [],
    'sb_snr_var_db': [],
    'wb_cqi_mean': [],
    'wb_cqi_mode': [],
    'wb_cqi_delta': [],
    'sb_cqi_mean': [],
    'sb_cqi_mode': [],
    'sb_cqi_delta': [],
}

combined_results = {
    'bw': [],
    'target_snr': [],
    'punctured_sc': [],
    'wb_cqi_count_0': [],
    'wb_cqi_count_1': [],
    'wb_cqi_count_2': [],
    'wb_cqi_count_3': [],
    'wb_cqi_count_4': [],
    'wb_cqi_count_5': [],
    'wb_cqi_count_6': [],
    'wb_cqi_count_7': [],
    'wb_cqi_count_8': [],
    'wb_cqi_count_9': [],
    'wb_cqi_count_10': [],
    'wb_cqi_count_11': [],
    'wb_cqi_count_12': [],
    'wb_cqi_count_13': [],
    'wb_cqi_count_14': [],
    'wb_cqi_count_15': [],
    'sb_cqi_count_0': [],
    'sb_cqi_count_1': [],
    'sb_cqi_count_2': [],
    'sb_cqi_count_3': [],
    'sb_cqi_count_4': [],
    'sb_cqi_count_5': [],
    'sb_cqi_count_6': [],
    'sb_cqi_count_7': [],
    'sb_cqi_count_8': [],
    'sb_cqi_count_9': [],
    'sb_cqi_count_10': [],
    'sb_cqi_count_11': [],
    'sb_cqi_count_12': [],
    'sb_cqi_count_13': [],
    'sb_cqi_count_14': [],
    'sb_cqi_count_15': [],
}

all_eff_sb_snr_columns = '"sb_0_eff_snr", "sb_1_eff_snr", "sb_2_eff_snr", "sb_3_eff_snr", "sb_4_eff_snr", "sb_5_eff_snr",' \
                      '"sb_6_eff_snr","sb_7_eff_snr","sb_8_eff_snr", "sb_9_eff_snr", "sb_10_eff_snr", "sb_11_eff_snr", "sb_12_eff_snr"'

all_eff_snr_columns = '"wb_eff_snr", "sb_0_eff_snr", "sb_1_eff_snr", "sb_2_eff_snr", "sb_3_eff_snr", "sb_4_eff_snr", "sb_5_eff_snr",' \
                      '"sb_6_eff_snr","sb_7_eff_snr","sb_8_eff_snr", "sb_9_eff_snr", "sb_10_eff_snr", "sb_11_eff_snr", "sb_12_eff_snr"'
