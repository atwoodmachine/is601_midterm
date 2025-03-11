# pylint: disable=unused-variable, invalid-name
'''Test set up for use with faker generated data'''

def test_calculation_operation(a, b, command, expected, capfd):
    '''Tests calculation result'''
    out = command.execute(a, b)
    assert out == expected
