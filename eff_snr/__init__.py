import eff_snr.constants
import eff_snr.config
import eff_snr.config.config_cli
import eff_snr.config.config_gui
import eff_snr.eff_snr_generator
import eff_snr.data.database_helper
from sys import argv


def main():
    config.config.initialize_result_dir()
    config.config.initialize_root_dir()

    print("4", config.config.DEFAULT_CONFIG_DIR)

    args = config.config_cli.parse_cli()
    if len(argv) == 1:
        args = config.config_gui.get_config()

    # eff_snr_generator.generate_eesm_distribution(2, '10', -3, 0, distance=1)