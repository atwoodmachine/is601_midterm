from decimal import Decimal
from calculator.commands import Command

class SubtractCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b

    def description(self):
        return "Subtract two operands: a - b"
    
    def usage(self):
        return "subtract <operand_a> <operand_b>"