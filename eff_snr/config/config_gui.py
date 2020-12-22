import tkinter as tk
from eff_snr.config.config import SIMULATION_CONFIG
from tkinter import filedialog
from eff_snr.config import config
import configparser
import os

global SIMULATION_CONFIG


def get_config():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


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
        self.create_widgets()
        self.master.geometry("600x300")
        self.master.title("Effective SNR calculator")

    def save_input_values(self):
        SIMULATION_CONFIG['data_storage_type'] = self.data_storage_type.get()
        SIMULATION_CONFIG['bw'].extend(list(self.bandwidths))
        SIMULATION_CONFIG['target_snr'].extend(self.get_snr_range(self.snr_range_entry.get()))
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

        with open(config.RESULTS_DIR + "config.ini", 'w') as f:
            parser.write(f)

        self.master.destroy()

    def use_default_settings(self):
        with open(config.DEFAULT_CONFIG_DIR) as config_file:
            self.parse_config_file(config_file)
        self.master.destroy()

    def create_widgets(self):
        tk.Label(self.master,
                 text="Type in your configuration and save or use default settings with 'Use default config' button.",
                 justify=tk.CENTER)\
            .grid(row=0, columnspan=2, pady=5, padx=0)

        self.data_storage_type = tk.StringVar()
        tk.Label(self.master, text="Data storage type: ", anchor="w", justify=tk.LEFT, width=21).grid(row=1, column=0)
        tk.Radiobutton(self.master, text="sqlite3", padx=20, variable=self.data_storage_type, value="sqlite3")\
            .grid(row=2, column=0)
        tk.Radiobutton(self.master, text="csv", padx=20, variable=self.data_storage_type, value="csv")\
            .grid(row=2, column=1)

        bandwidth_checkbar_picks = ['5', '10', '15', '20']
        tk.Label(self.master, text="Bandwidth selection [MHz]:", anchor="w", justify=tk.LEFT, width=21)\
            .grid(row=3, column=0)
        bw_checkbar = Checkbar(self.master, bandwidth_checkbar_picks)
        bw_checkbar.grid(row=3, column=1)
        self.bandwidths = bw_checkbar.state()

        tk.Label(self.master, text="SNR range (a,b:c) [dB]: ", anchor="w", justify=tk.LEFT, width=21).grid(row=4)
        self.snr_range_entry = tk.Entry(self.master)
        self.snr_range_entry.grid(row=4, column=1)

        tk.Label(self.master, text="No of punctured sc [%]: ", anchor="w", justify=tk.LEFT, width=21)\
            .grid(row=5, column=0)
        self.no_of_punctured_resources_entry = tk.Entry(self.master)
        self.no_of_punctured_resources_entry.grid(row=5, column=1)

        self.puncturing_location = tk.StringVar()
        tk.Label(self.master, text="Puncturing: ", anchor="w", justify=tk.LEFT, width=21).grid(row=7, column=0)
        tk.Radiobutton(self.master, text="Lower edge", padx=20, variable=self.puncturing_location, value="low")\
            .grid(row=8, column=0)
        tk.Radiobutton(self.master, text="Upper edge", padx=20, variable=self.puncturing_location, value="high")\
            .grid(row=8, column=1)
        tk.Radiobutton(self.master, text="Both edges", padx=20, variable=self.puncturing_location, value="both")\
            .grid(row=8, column=2)

        tk.Label(self.master, text="Pathloss exponent: ", anchor="w", justify=tk.LEFT, width=21).grid(row=9, column=0)
        self.pl_exp_entry = tk.Entry(self.master)
        self.pl_exp_entry.grid(row=9, column=1)

        tk.Label(self.master, text="Distance [m]: ", anchor="w", justify=tk.LEFT, width=21).grid(row=10, column=0)
        self.distance_entry = tk.Entry(self.master)
        self.distance_entry.grid(row=10, column=1)

        tk.Label(self.master, text="Number of Repetitions: ", anchor="w", justify=tk.LEFT, width=21).grid(row=11)
        self.repetitions_entry = tk.Entry(self.master)
        self.repetitions_entry.grid(row=11, column=1)

        button_quit = tk.Button(self.master, text="Quit", fg="black", command=self.master.destroy,
                                anchor="w", justify=tk.LEFT, width=5)
        button_quit.grid(row=12, column=0)

        buttons_frame = tk.Frame(self.master)
        button_save_cont = tk.Button(buttons_frame, text="Save config", fg="black", command=self.save_input_values,
                                     anchor="w", justify=tk.LEFT, width=10)
        button_save_cont.pack(side=tk.LEFT, expand=True, padx=(10, 10), pady=10)

        button_cont_default = tk.Button(buttons_frame, text="Use default config", fg="black",
                                        command=self.use_default_settings, anchor="w", justify=tk.LEFT, width=15)
        button_cont_default.pack(side=tk.LEFT, expand=True, padx=(10, 10), pady=10)

        button_cont_from_file = tk.Button(buttons_frame, text="Use config from file", fg="black",
                                          command=self.select_path, anchor="w", justify=tk.LEFT, width=15)
        button_cont_from_file.pack(side=tk.LEFT, expand=True, padx=(10, 10), pady=10)
        buttons_frame.grid(row=12, column=1, columnspan=2)

    def select_path(self):
        filename = filedialog.askopenfilename(filetypes=[("ini files", "*.ini")])
        with open(filename) as config_file:
            self.parse_config_file(config_file)
        self.master.destroy()


class Checkbar(tk.Frame):
    def __init__(self, parent=None, picks=[], side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, offvalue='0', onvalue=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)
