#pylint: disable=unused-variable
'''Tests commands with simulated user input'''
import pytest
from calculator import Calculator

def test_exit_command(capfd, monkeypatch):
    '''Tests proper exit from program'''
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    calc = Calculator()
    with pytest.raises(SystemExit) as e:
        calc.start()
    assert e.type == SystemExit

def test_unknown_command(capfd, monkeypatch):
    '''Tests unrecognized command entered'''
    inputs = iter(['err', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    calc = Calculator()
    with pytest.raises(SystemExit) as e:
        calc.start()
    output = capfd.readouterr()
    assert "Command not recognized: err" in output.out

def test_argument_number_error(capfd, monkeypatch):
    '''Tests too few arguments entered'''
    inputs = iter(['add 1', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    calc = Calculator()
    with pytest.raises(SystemExit) as e:
        calc.start()
    output = capfd.readouterr()
    assert "missing" in output.out

def test_argument_type_error(capfd, monkeypatch):
    '''Tests argument type error'''
    inputs = iter(['add 1 a', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    calc = Calculator()
    with pytest.raises(SystemExit) as e:
        calc.start()
    output = capfd.readouterr()
    assert "Error: argument entered was not a valid number" in output.out

def test_menu(capfd, monkeypatch):
    '''Tests menu command'''
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    calc = Calculator()
    with pytest.raises(SystemExit) as e:
        calc.start()
    output = capfd.readouterr()
    assert "---Available Calculator Commands---" in output.out
