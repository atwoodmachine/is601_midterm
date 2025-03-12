import ast
from calculator.commands import Command
from calculator.historyManager import HistoryManager

class DeleteHistoryCommand(Command):
    def execute(self, *args):
        command_name = args[0] if len(args) > 0 else None
        try:
            arguments = [float(arg) for arg in args[1:]] if len(args) > 1 else None
        except ValueError:
            print(f"Invalid argument(s): {args}, please enter command as deletehistory <operation> <optional: operand1 operand2>")
            return

        df_history = HistoryManager.get_history_as_df()

        if df_history is not None and not df_history.empty:
            if command_name and arguments: 
                df_history['Arguments'] = df_history['Arguments'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

                filter_condition = (
                    (df_history['Operation'].str.fullmatch(command_name, case=False, na=False)) &
                    (df_history['Arguments'].apply(lambda x: list(x) == arguments))
                )
                df_history_filtered = df_history[filter_condition]

            elif command_name:
                filter_condition = df_history['Operation'].str.fullmatch(command_name, case=False, na=False)
                df_history_filtered = df_history[filter_condition]
            else:
                print("Error: Command name is required for deletion.")
                return

            if not df_history_filtered.empty:
                df_history = df_history[~filter_condition]
                HistoryManager.save_to_history(df_history)

                print(f"Successfully deleted {len(df_history_filtered)} matching row(s) from history.")
            else:
                print(f"No matching history found for command '{command_name}' with arguments {arguments}.")
        else:
            print("History is empty")
    
    def description(self):
        return "Delete history based on command name and optional arguments"
    
    def usage(self):
        return "deletehistory <command_name> <optional: arguments>"

