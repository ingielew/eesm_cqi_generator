import argparse
import sys


def parse_cli():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--bandwidth",
            type=list,
            default=['5', '10', '15', '20'],
            help="Bandwidths to generate effective SNR for. Default -- all bandwidths >= 5MHz",
        )
        return parser.parse_args()
    except argparse.ArgumentError as err:
        print(str(err))
        sys.exit(2)
