'''Test the history manipulation commands history, clearhistory, deletehistory'''
from unittest.mock import patch
import pytest
import pandas as pd
from calculator.historyManager import HistoryManager
from calculator.plugins.history import HistoryCommand

@pytest.fixture
def mock_history_data():
    '''Mock history data for testing'''
    data = {
        'Operation': ['add', 'subtract', 'multiply', 'divide'],
        'Arguments': ['[1, 2]', '[5, 3]', '[4, 6]', '[8, 2]'],
        'Result': [3, 2, 24, 4]
    }
    return pd.DataFrame(data)

def test_history_command(mock_history_data):
    '''Test history command returns all history'''
    with patch.object(HistoryManager, 'get_history_as_df', return_value=mock_history_data):
        with patch('builtins.print') as mock_print:
            command = HistoryCommand()
            command.execute()
            mock_print.assert_called_with(mock_history_data.to_string())

def test_history_filters_by_command(mock_history_data):
    '''Test with command argument for filtered history'''
    with patch.object(HistoryManager, 'get_history_as_df', return_value=mock_history_data):
        with patch('builtins.print') as mock_print:
            command = HistoryCommand()
            command.execute('add')
            filtered_data = mock_history_data[mock_history_data['Operation'].str.fullmatch('add', case=False)]
            mock_print.assert_called_with(filtered_data.to_string())

def test_history_command_no_matching_results(mock_history_data):
    '''Test no matches prints no matching results'''
    with patch.object(HistoryManager, 'get_history_as_df', return_value=mock_history_data):
        with patch('builtins.print') as mock_print:
            command = HistoryCommand()
            command.execute('nonexistent_command')
            mock_print.assert_called_with("No matching results found")

def test_history_command_empty_history():
    '''Test empty dataframe returns no matching results'''
    with patch.object(HistoryManager, 'get_history_as_df', return_value=pd.DataFrame()):
        with patch('builtins.print') as mock_print:
            command = HistoryCommand()
            command.execute()
            mock_print.assert_called_with("No matching results found")
