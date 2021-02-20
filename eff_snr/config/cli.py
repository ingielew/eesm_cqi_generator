import argparse
import sys
from .common import SIMULATION_CONFIG


def convert_args_into_sim_config(parsed_args):
    sim_config = SIMULATION_CONFIG

    if parsed_args.generate is True:
        sim_config = None
    elif parsed_args.process_results is True:
        sim_config['generate'] = False
        sim_config['process_results'] = True
        sim_config['process_data_file'] = parsed_args.file
        sim_config['bw'] = parsed_args.bandwidth.split(',')
    return sim_config


def parse_cli():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--bandwidth",
            type=str,
            help="Bandwidths to generate effective SNR for. Default -- all bandwidths >= 5MHz"
        )
        parser.add_argument(
            "--file",
            type=str,
            # action="store_true",
            help="Effective-SINR mapped file location to be processed."
        )
        parser.add_argument(
            "--generate",
            type=bool,
            # action="store_true",
            help="Set to '1' to generate the ESM data"
        )
        parser.add_argument(
            "--process_results",
            type=bool,
            # action="store_true",
            help="Set to '0' to process generated results"
        )
        return convert_args_into_sim_config(parser.parse_args())
    except argparse.ArgumentError as err:
        print(str(err))
        sys.exit(2)
