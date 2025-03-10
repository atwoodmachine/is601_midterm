import logging
import os
import pandas as pd

class HistoryManager:
    HISTORY_DIR = './history'
    @classmethod
    def initialize_history(cls):
        if not os.path.exists(cls.HISTORY_DIR):
            os.makedirs(cls.HISTORY_DIR)
            logging.info(f"History directory created: {cls.HISTORY_DIR}")
        elif not os.access(cls.HISTORY_DIR, os.W_OK):
            logging.error(f"The directory {cls.HISTORY_DIR} is not writeable")
            return
    @classmethod
    def add_to_history(cls, command_name:str, args, result, filename = 'calculation_history.csv'):
        calc = {'Operation': [command_name], 'Arguments': [args], 'Result': [result]}
        df_calc = pd.DataFrame(calc)
        csv_file_path = os.path.join(cls.HISTORY_DIR, filename)
        if os.path.exists(csv_file_path):
            df_calc.to_csv(csv_file_path, mode='a', header=False, index=False)
        else:
            logging.info(f"Created history file {filename}")
            df_calc.to_csv(csv_file_path, mode='w', header=True, index=False)