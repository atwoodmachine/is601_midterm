from decimal import Decimal
from calculator.commands import Command
from calculator.historyManager import HistoryManager

class HistoryCommand(Command):
    def execute(self):
        df_history = HistoryManager.get_history_as_df()
        if df_history is not None and not df_history.empty:
            print(df_history.to_string())
        else:
            print("History is empty")
    
    def description(self):
        return "Returns every calculation in calculation history"
    
    def usage(self):
        return "history"