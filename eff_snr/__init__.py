import eff_snr.constants
import eff_snr.config
import eff_snr.config.config_cli
import eff_snr.config.config_gui
import eff_snr.eff_snr_generator
import eff_snr.data_preprocessor
from sys import argv


def main():
    config.common_config.initialize_result_dir()
    config.common_config.initialize_root_dir()

    sim_config = config.config_cli.parse_cli()
    if len(argv) == 1:
        sim_config = config.config_gui.get_config()
    print(sim_config)

    if sim_config['generate'] is True:
        eff_snr_generator.main(sim_config)
    elif sim_config['process_results'] is True:
        data_preprocessor.main(sim_config['process_data_file'])
