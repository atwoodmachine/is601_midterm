from decimal import Decimal
from calculator.commands import Command

class MultiplyCommand(Command):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b

    def description(self):
        return "Multiply two operands: a * b"
    
    def usage(self):
        return "multiply <operand_a> <operand_b>"