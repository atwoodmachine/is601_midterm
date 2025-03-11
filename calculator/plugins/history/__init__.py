from decimal import Decimal
from calculator.commands import Command
from calculator.historyManager import HistoryManager

class HistoryCommand(Command):
    def execute(self, *args):
        command_name = args[0] if len(args) > 0 else None

        df_history = HistoryManager.get_history_as_df()
        if command_name:
            df_history = df_history[df_history['Operation'].str.fullmatch(command_name, case=False, na=False)]
        
        if df_history is not None and not df_history.empty:
            print(df_history.to_string())
        else:
            print("No matching results found")
    
    def description(self):
        return "Default: Returns every calculation in calculation history\nhistory <operation> filters result by operation"
    
    def usage(self):
        return "history <optional: operation>"