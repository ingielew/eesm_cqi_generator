import tkinter as tk
from eff_snr.config.common import SIMULATION_CONFIG
from tkinter import filedialog
from eff_snr.config import common
import configparser
import os


def get_config():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    return SIMULATION_CONFIG


class Application(tk.Frame):
    puncturing_location = None
    data_storage_type = None
    bandwidths = None
    distance_entry = None
    pl_exp_entry = None
    no_of_punctured_resources_entry = None
    snr_range_entry = None
    repetitions_entry = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.prompt_generate_process()
        self.master.geometry("460x75")
        self.master.title("Effective SNR calculator")

        self.process_data_file = ""

    def save_input_generator_values(self):
        SIMULATION_CONFIG['data_storage_type'] = self.data_storage_type.get()
        SIMULATION_CONFIG['bw'].extend(list(self.bandwidths))
        SIMULATION_CONFIG['target_snr'].extend(common.get_snr_range(self.snr_range_entry.get()))
        SIMULATION_CONFIG['punctured_sc'] = self.no_of_punctured_resources_entry.get()
        SIMULATION_CONFIG['puncturing_area'] = self.puncturing_location.get()
        SIMULATION_CONFIG['pathloss_exp'] = self.pl_exp_entry.get()
        SIMULATION_CONFIG['distance'] = self.distance_entry.get()
        SIMULATION_CONFIG['repetitions'] = self.repetitions_entry.get()

        parser = configparser.ConfigParser()
        parser.add_section('Simulation Config')
        for key in SIMULATION_CONFIG.keys():
            parser.set('Simulation Config', key, str(SIMULATION_CONFIG[key]))

        with open('config.ini', 'w') as f:
            parser.write(f)

        with open(common.RESULTS_DIR + "config.ini", 'w') as f:
            parser.write(f)

        self.master.destroy()

    def save_processor_config(self):
        SIMULATION_CONFIG['process_results'] = True
        SIMULATION_CONFIG['bw'].extend(list(self.bandwidths))
        SIMULATION_CONFIG['process_data_file'] = self.process_data_file
        self.master.destroy()

    def use_default_settings(self):
        with open(common.DEFAULT_CONFIG_DIR) as config_file:
            common.parse_config_file(config_file)
        self.master.destroy()

    def prompt_generate_process(self):
        tk.Label(self.master,
                 text="Select between generating new set of data, or processing existing one.",
                 justify=tk.CENTER) \
            .grid(row=0, columnspan=2, pady=5, padx=10)

        tk.Button(self.master, text="Quit", fg="black", command=self.master.destroy,
                  anchor="w", justify=tk.CENTER, width=5).grid(row=1, column=0)
        tk.Button(self.master, text='Generate', command=self.create_generator_widgets).grid(row=1, column=1)
        tk.Button(self.master, text='Process', command=self.create_processor_widgets).grid(row=1, column=2)

    def create_processor_widgets(self):
        window = tk.Toplevel(self.master)
        window.geometry("400x150")
        bandwidth_checkbar_picks = ['5', '10', '15', '20']
        tk.Label(window,
                 text="Select data file for processing",
                 justify=tk.CENTER) \
            .grid(row=0, columnspan=2, pady=5, padx=0)

        tk.Label(window, text="Bandwidth selection [MHz]:", anchor="w", justify=tk.LEFT, width=21)\
            .grid(row=1, column=0)
        bw_checkbar = Checkbar(window, bandwidth_checkbar_picks)
        bw_checkbar.grid(row=1, column=1)
        self.bandwidths = bw_checkbar.state()

        path_select_label = tk.Label(window, text='<selected path>')
        path_select_label.grid(row=2, column=1, pady=5)

        def select_path_update_label():
            self.select_data_path()
            path_select_label.config(text=self.process_data_file[-40:])

        tk.Button(window, text="Filepath", fg="black", command=select_path_update_label,
                  anchor="w", justify=tk.CENTER).grid(row=2, column=0, pady=5)

        tk.Button(window, text="Quit", fg="black", command=self.master.destroy,
                  anchor="w", justify=tk.LEFT, width=5).grid(row=3, column=0, pady=5)
        tk.Button(window, text="Continue", fg="black", command=self.save_processor_config,
                  anchor="w", justify=tk.RIGHT).grid(row=3, column=1, pady=5)

    def create_generator_widgets(self):
        window = tk.Toplevel(self.master)
        window.geometry("650x350")
        tk.Label(window,
                 text="Type in your configuration and save or use default settings with 'Use default config' button.",
                 justify=tk.CENTER)\
            .grid(row=0, columnspan=2, pady=5, padx=0)
        SIMULATION_CONFIG['generate'] = True
        self.data_storage_type = tk.StringVar()
        tk.Label(window, text="Data storage type: ", anchor="w", justify=tk.LEFT, width=21).grid(row=1, column=0)
        tk.Radiobutton(window, text="sqlite3", padx=20, variable=self.data_storage_type, value="sqlite3")\
            .grid(row=2, column=0)
        tk.Radiobutton(window, text="csv", padx=20, variable=self.data_storage_type, value="csv")\
            .grid(row=2, column=1)

        bandwidth_checkbar_picks = ['5', '10', '15', '20']
        tk.Label(window, text="Bandwidth selection [MHz]:", anchor="w", justify=tk.LEFT, width=21)\
            .grid(row=3, column=0)
        bw_checkbar = Checkbar(window, bandwidth_checkbar_picks)
        bw_checkbar.grid(row=3, column=1)
        self.bandwidths = bw_checkbar.state()

        tk.Label(window, text="SNR range (a,b:c) [dB]: ", anchor="w", justify=tk.LEFT, width=21).grid(row=4)
        self.snr_range_entry = tk.Entry(window)
        self.snr_range_entry.grid(row=4, column=1)

        tk.Label(window, text="No of punctured sc [%]: ", anchor="w", justify=tk.LEFT, width=21)\
            .grid(row=5, column=0)
        self.no_of_punctured_resources_entry = tk.Entry(window)
        self.no_of_punctured_resources_entry.grid(row=5, column=1)

        self.puncturing_location = tk.StringVar()
        tk.Label(window, text="Puncturing: ", anchor="w", justify=tk.LEFT, width=21).grid(row=7, column=0)
        tk.Radiobutton(window, text="Lower edge", padx=20, variable=self.puncturing_location, value="low")\
            .grid(row=8, column=0)
        tk.Radiobutton(window, text="Upper edge", padx=20, variable=self.puncturing_location, value="high")\
            .grid(row=8, column=1)
        tk.Radiobutton(window, text="Both edges", padx=20, variable=self.puncturing_location, value="both")\
            .grid(row=8, column=2)

        tk.Label(window, text="Pathloss exponent: ", anchor="w", justify=tk.LEFT, width=21).grid(row=9, column=0)
        self.pl_exp_entry = tk.Entry(window)
        self.pl_exp_entry.grid(row=9, column=1)

        tk.Label(window, text="Distance [m]: ", anchor="w", justify=tk.LEFT, width=21).grid(row=10, column=0)
        self.distance_entry = tk.Entry(window)
        self.distance_entry.grid(row=10, column=1)

        tk.Label(window, text="Number of Repetitions: ", anchor="w", justify=tk.LEFT, width=21).grid(row=11)
        self.repetitions_entry = tk.Entry(window)
        self.repetitions_entry.grid(row=11, column=1)

        button_quit = tk.Button(window, text="Quit", fg="black", command=window.destroy,
                                anchor="w", justify=tk.LEFT, width=5)
        button_quit.grid(row=12, column=0)

        buttons_frame = tk.Frame(window)
        button_save_cont = tk.Button(buttons_frame, text="Save config", fg="black",
                                     command=self.save_input_generator_values, anchor="w", justify=tk.LEFT, width=10)
        button_save_cont.pack(side=tk.LEFT, expand=True, padx=(10, 10), pady=10)

        button_cont_default = tk.Button(buttons_frame, text="Use default config", fg="black",
                                        command=self.use_default_settings, anchor="w", justify=tk.LEFT, width=15)
        button_cont_default.pack(side=tk.LEFT, expand=True, padx=(10, 10), pady=10)

        button_cont_from_file = tk.Button(buttons_frame, text="Use config from file", fg="black",
                                          command=self.select_config_path, anchor="w", justify=tk.LEFT, width=15)
        button_cont_from_file.pack(side=tk.LEFT, expand=True, padx=(10, 10), pady=10)
        buttons_frame.grid(row=12, column=1, columnspan=2)

    def select_config_path(self):
        filename = filedialog.askopenfilename(filetypes=[("ini files", "*.ini")])
        with open(filename) as config_file:
            common.parse_config_file(config_file)
        self.master.destroy()

    def select_data_path(self):
        filename = filedialog.askopenfilename(filetypes=[("data files", "*.db", "*csv")])
        self.process_data_file = os.path.abspath(filename)


class Checkbar(tk.Frame):
    def __init__(self, parent, picks, side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, offvalue='0', onvalue=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)
