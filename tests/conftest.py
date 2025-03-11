#pylint: disable=comparison-with-callable
'''Configure faker testing for command line'''
import io
from contextlib import redirect_stdout
from decimal import Decimal
from faker import Faker
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.multiply import MultiplyCommand

fake = Faker()

def generate_test_data(num_records):
    '''Generates test data based on number of records defined in command line'''
    operation_mappings = {
        'add': AddCommand(),
        'subtract': SubtractCommand(),
        'multiply': MultiplyCommand(),
        'divide': DivideCommand()
    }

    for i in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        if i % 3 == 0:
            b = Decimal(fake.random_number(digits=2))
        else:
            b = Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        command = operation_mappings[operation_name]

        if isinstance(command, DivideCommand) and b == 0:
            b = Decimal("1")

        with io.StringIO() as buf, redirect_stdout(buf):
            expected = command.execute(a, b)

        yield a, b, operation_name, command, expected

def pytest_addoption(parser):
    '''Adds num_records as command line option'''
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    '''Generates and runs tests in test_calculation.py with generated tests'''
    if {"a", "b", "command"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        modified_parameters = [(a, b, command if 'operation_name' in metafunc.fixturenames else op_func, expected) for a, b, command, op_func, expected in parameters]
        metafunc.parametrize("a,b,command,expected", modified_parameters)
