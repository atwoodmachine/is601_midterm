from decimal import Decimal
from calculator.commands import Command

class AddCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b
    
    def description(self):
        return "Add two operands: a + b"
    
    def usage(self):
        return "add <operand_a> <operand_b>"