import eff_snr.constants

import eff_snr.eff_snr_generator
import eff_snr.data_preprocessor
from sys import argv

from .config import common as common_config
from .config import cli as cli_config
from .config import gui as gui_config


def main():
    common_config.initialize_result_dir_path()
    common_config.initialize_root_dir()

    if len(argv) == 1:
        sim_config = gui_config.get_config()
    else:
        sim_config = cli_config.parse_cli()

    if sim_config is not None:
        print(sim_config)
        if sim_config['generate'] is True:
            eff_snr_generator.main(sim_config)
        elif sim_config['process_results'] is True:
            data_preprocessor.main(sim_config)
