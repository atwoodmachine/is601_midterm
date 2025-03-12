import logging
import os
import pandas as pd
from dotenv import load_dotenv

class HistoryManager:
    load_dotenv()
    logging.info("HistoryManager: loaded environment variables")
    HISTORY_DIR = os.getenv('HISTORY_DIR', './history')
    HISTORY_FILE = os.getenv('HISTORY_FILE', 'calculation_history.csv')
   
    @classmethod
    def initialize_history(cls):
        if not os.path.exists(cls.HISTORY_DIR):
            os.makedirs(cls.HISTORY_DIR)
            logging.info(f"History directory created: {cls.HISTORY_DIR}")
        elif not os.access(cls.HISTORY_DIR, os.W_OK):
            logging.error(f"The directory {cls.HISTORY_DIR} is not writeable")
            return
        if not os.path.exists(os.path.join(cls.HISTORY_DIR, cls.HISTORY_FILE)):
            df = pd.DataFrame(columns=["Operation", "Arguments", "Result"])
            df.to_csv(HistoryManager.get_history_path(), index=False)
            logging.info(f"History file created at {HistoryManager.get_history_path()}")
   
    @classmethod
    def add_to_history(cls, command_name:str, args, result):
        display_args = [float(arg) for arg in args]

        calc = {'Operation': [command_name], 'Arguments': [display_args], 'Result': [result]}
        df_calc = pd.DataFrame(calc)
        csv_file_path = os.path.join(cls.HISTORY_DIR, cls.HISTORY_FILE)
        if os.path.exists(csv_file_path):
            df_calc.to_csv(csv_file_path, mode='a', header=False, index=False)
        else:
            df_calc.to_csv(csv_file_path, mode='w', header=True, index=False)
            logging.info(f"Created history file {cls.HISTORY_FILE}")

    @classmethod
    def get_history_as_df(cls):
        csv_file_path = os.path.join(cls.HISTORY_DIR, cls.HISTORY_FILE)
        try:
            df_history = pd.read_csv(csv_file_path)
            return df_history 
        except FileNotFoundError:
            logging.error(f"Error: The file '{csv_file_path}' was not found.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        return None

    @classmethod
    def get_history_path(cls):
        return os.path.join(cls.HISTORY_DIR, cls.HISTORY_FILE)
    
    @classmethod
    def save_to_history(cls, df):
        csv_file_path = os.path.join(cls.HISTORY_DIR, cls.HISTORY_FILE)
        df.to_csv(csv_file_path, mode='w', header=True, index=False)
