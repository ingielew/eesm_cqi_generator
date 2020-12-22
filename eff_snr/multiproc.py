# from eff_snr.data.database import Database
# from eesm_parser import Parser
# import multiprocessing
# from os import cpu_count
# from eff_snr.constants import data_ranges
# from eff_snr import eff_snr_generator
#
#
# def eesm_process(bandwidth, tar_snr):
#     print("Gen Called for bw:", bandwidth, "SNR: ", tar_snr)
#     #data_generator = create_generator()
#     for punctured_sc in data_ranges['punctured_sc_{}Mhz'.format(bandwidth)]:
#         for repetition in range(0, 1):
#             eff_snr_generator.generate_eesm_distribution(2, bandwidth, tar_snr, punctured_sc, distance=1)
#     #data_generator.commit_results_to_db()
#
#
# def parse_process(bandwidth, tar_snr):
#     print("Par Called for bw:", bandwidth, "SNR: ", tar_snr)
#     parser = create_parser()
#     parser.handle_subband_results(bandwidth, tar_snr)
#
#
# def create_generator():
#     database = Database()
#     eff_snr_data_generator = eff_snr_generator.generate_eesm_distribution()
#     return eff_snr_data_generator
#
#
# def create_parser():
#     database = Database()
#     parser = Parser(database)
#     return parser
#
#
# if __name__ == '__main__':
#     bw = ['5', '10', '15', '20']
#     input_proc = []
#     generate_data = True
#     parse = True
#
#     for bandwidths in bw:
#         for target_snr in data_ranges['target_snr']:
#             input_proc.append((bandwidths, target_snr))
#

    # data_generator = create_generator()
    # data_generator.generate_eesm_distribution(2, '5', -9, 48)
    # input_proc.append(['20', 21])
    # if generate_data:
    #     with multiprocessing.Pool(cpu_count()) as pool:
    #         # pool.starmap(eesm_process, tuple(input_proc))
    #         pool.starmap(eesm_process, tuple(input_proc))
    # if parse:
    #     parse_process('20', 19)
    #     for bandw in bw:
    #         for snr in data_ranges['target_snr']:
    #             parse_process(bandw, snr)

    # print(input_proc)
    # if parse:
    #     with multiprocessing.Pool(cpu_count()) as pool:
    #         pool.starmap(parse_process, tuple(input_proc))
