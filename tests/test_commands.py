# pylint: disable=unused-variable
'''Tests for command plugins for math operations'''
from decimal import Decimal
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.multiply import MultiplyCommand

def test_add_command(capfd):
    '''Tests addition'''
    command = AddCommand()
    command.execute(Decimal('1'), Decimal('2'))
    out, err = capfd.readouterr()
    assert out == "Result: 3\n", "Failed addition, should output 'Result: 3'"

def test_subtract_command(capfd):
    '''Tests subtration'''
    command = SubtractCommand()
    command.execute(Decimal('9'), Decimal('4'))
    out, err = capfd.readouterr()
    assert out == "Result: 5\n", "Failed subtraction, should output 'Result: 5'"

def test_multiply_command(capfd):
    '''Tests multiplication'''
    command = MultiplyCommand()
    command.execute(Decimal('5'), Decimal('4'))
    out, err = capfd.readouterr()
    assert out == "Result: 20\n", "Failed multiplication, should output 'Result: 20'"

def test_divide_command(capfd):
    '''Tests division'''
    command = DivideCommand()
    command.execute(Decimal('20'), Decimal('2'))
    out, err = capfd.readouterr()
    assert out == "Result: 10\n", "Failed subtraction, should output 'Result: 10'"

def test_divide_by_zero(capfd):
    '''Tests division by zero throws error correctly'''
    command = DivideCommand()
    command.execute(Decimal('10'), Decimal('0'))
    out, err = capfd.readouterr()
    assert out == "Math error: division by zero\n", "Failed division by zero, should throw error 'Math error: division by zero'"
