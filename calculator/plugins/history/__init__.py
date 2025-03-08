from decimal import Decimal
from calculator.commands import Command

class HistoryCommand(Command):
    def execute(self):
        pass
    
    def description(self):
        return "Returns every calculation in calculation history"
    
    def usage(self):
        return "history"