import pandas as pd
from calculator.commands import Command
from calculator.historyManager import HistoryManager

class ClearHistoryCommand(Command):
    def execute(self):
        df = pd.DataFrame(columns=["Operation", "Arguments", "Result"])
        df.to_csv(HistoryManager.get_history_path(), index=False)
        print("Calculation history cleared.")
    
    def description(self):
        return "Clears every calculation in calculation history"
    
    def usage(self):
        return "clearhistory"
