import os
import datetime
import errno
import configparser

SIMULATION_CONFIG = {
    'data_storage_type': "",
    'bw': [],
    'target_snr': [],
    'punctured_sc': 0,
    'puncturing_area': 0,
    'pathloss_exp': 0,
    'distance': 0,
    'repetitions': 0,
    'generate': 0,
    'process_results': 0,
    'process_data_file': ""
}

RESULTS_DIR = ""
ROOT_DIR = ""
DEFAULT_CONFIG_DIR = ""


def initialize_result_dir():
    global RESULTS_DIR
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    RESULTS_DIR = os.path.join(os.getcwd(), "results", timestamp)
    try:
        os.mkdir(RESULTS_DIR)
    except OSError as os_error:
        if os_error.errno != errno.EEXIST:
            raise
    print(RESULTS_DIR)


def initialize_root_dir():
    global ROOT_DIR
    global DEFAULT_CONFIG_DIR
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_CONFIG_DIR = os.path.join(ROOT_DIR, '', 'simulation_default_config.ini')


def parse_config_file(config_file):
    parser = configparser.ConfigParser()
    parser.read_file(config_file)
    SIMULATION_CONFIG['data_storage_type'] = parser['Simulation Config']['data_storage_type']
    SIMULATION_CONFIG['bw'] = parser['Simulation Config']['bw']
    SIMULATION_CONFIG['target_snr'] = parser['Simulation Config']['target_snr']
    SIMULATION_CONFIG['punctured_sc'] = parser['Simulation Config']['punctured_sc']
    SIMULATION_CONFIG['puncturing_area'] = parser['Simulation Config']['puncturing_area']
    SIMULATION_CONFIG['pathloss_exp'] = parser['Simulation Config']['pathloss_exp']
    SIMULATION_CONFIG['distance'] = parser['Simulation Config']['distance']
    SIMULATION_CONFIG['repetitions'] = parser['Simulation Config']['repetitions']

    with open(os.path.join(RESULTS_DIR, "config.ini"), 'w') as f:
        parser.write(f)


def get_snr_range(snr_range_entry_val):
    result = []
    for part in snr_range_entry_val.split(','):
        if ':' in part:
            a, b = part.split(':')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
        else:
            a = int(part)
            result.append(a)

    if 0 in result:
        result.remove(0)  # SNR in dB, 0 not allowed.
    return result


def join_paths(path_1, path_2):
    return os.path.join(path_1, path_2)
