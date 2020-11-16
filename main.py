from database import Database
from eesm_parser import Parser

from eff_snr_eesm_generator import EffSnrEesmGenerator
import multiprocessing
from os import cpu_count
from constants import data_ranges, num_repetitions


def eesm_process(bandwidth, tar_snr):
    print("Called for bw:", bandwidth, "SNR: ", tar_snr)
    data_generator = create_generator()
    for punctured_sc in data_ranges['punctured_sc_{}Mhz'.format(bandwidth)]:
        for repetition in range(0, num_repetitions):
            data_generator.generate_eesm_distribution(2, bandwidth, tar_snr, punctured_sc)
    data_generator.commit_results_to_db()


def parse_process(bandwidth, tar_snr):
    print("Called for bw:", bandwidth, "SNR: ", tar_snr)
    parser = create_parser()
    parser.handle_subband_results(bandwidth, tar_snr)


def create_generator():
    database = Database()
    eff_snr_data_generator = EffSnrEesmGenerator(database)
    return eff_snr_data_generator


def create_parser():
    database = Database()
    parser = Parser(database)
    return parser


if __name__ == '__main__':
    bw = ['5', '10', '15', '20']
    input_proc = []
    generate_data = True
    parse = False

    for bandwidths in bw:
        for target_snr in data_ranges['target_snr']:
            input_proc.append((bandwidths, target_snr))

    if generate_data:
        with multiprocessing.Pool(cpu_count()) as pool:
            pool.starmap(eesm_process, tuple(input_proc))

    if parse:
        with multiprocessing.Pool(cpu_count()) as pool:
            pool.starmap(parse_process, tuple(input_proc))
