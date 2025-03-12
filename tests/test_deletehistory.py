'''Test history manipulation command deletehistory'''
import os
import tempfile
from unittest.mock import patch
import pytest
import pandas as pd
from calculator.historyManager import HistoryManager
from calculator.plugins.deletehistory import DeleteHistoryCommand

@pytest.fixture
def setup_test_history():
    '''Setup a temporary history file for testing'''
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch.object(HistoryManager, 'HISTORY_DIR', temp_dir), \
             patch.object(HistoryManager, 'HISTORY_FILE', 'test_calculation_history.csv'):

            data = {
                'Operation': ['add', 'subtract', 'multiply', 'divide'],
                'Arguments': ['[1, 2]', '[5, 3]', '[4, 6]', '[8, 2]'],
                'Result': [3, 2, 24, 4]
            }
            df = pd.DataFrame(data)

            os.makedirs(HistoryManager.HISTORY_DIR, exist_ok=True)
            df.to_csv(HistoryManager.get_history_path(), index=False)

            yield df

def test_delete_history_by_command_name(setup_test_history):
    '''Test deleting entries by command name'''
    command = DeleteHistoryCommand()

    with patch('builtins.print') as mock_print:
        command.execute('add')
        df = HistoryManager.get_history_as_df()
        assert len(df) == 3, "Entry was not deleted correctly."
        assert 'add' not in df['Operation'].values, "Command 'add' was not deleted."
        mock_print.assert_called_with("Successfully deleted 1 matching row(s) from history.")

def test_delete_history_by_command_and_arguments(setup_test_history):
    '''Test deleting entries by command and arguments'''
    command = DeleteHistoryCommand()

    with patch('builtins.print') as mock_print:
        command.execute('subtract', '5', '3')

        # Reload the history and confirm deletion
        df = HistoryManager.get_history_as_df()
        assert len(df) == 3, "Entry was not deleted correctly."
        assert not ((df['Operation'] == 'subtract') & (df['Arguments'] == '[5, 3]')).any()
        mock_print.assert_called_with("Successfully deleted 1 matching row(s) from history.")

def test_delete_history_no_match(setup_test_history):
    '''Test when no matching entry is found'''
    command = DeleteHistoryCommand()

    with patch('builtins.print') as mock_print:
        command.execute('modulus')
        df = HistoryManager.get_history_as_df()
        assert len(df) == 4, "History should remain unchanged."
        mock_print.assert_called_with("No matching history found for command 'modulus' with arguments None.")

def test_delete_history_missing_command(setup_test_history):
    '''Test when command name is missing'''
    command = DeleteHistoryCommand()

    with patch('builtins.print') as mock_print:
        command.execute()

        df = HistoryManager.get_history_as_df()
        assert len(df) == 4, "History should remain unchanged."
        mock_print.assert_called_with("Error: Command name is required for deletion.")

def test_delete_history_empty_history():
    '''Test deleting from an empty history'''
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch.object(HistoryManager, 'HISTORY_DIR', temp_dir), \
             patch.object(HistoryManager, 'HISTORY_FILE', 'test_calculation_history.csv'):

            command = DeleteHistoryCommand()

            with patch('builtins.print') as mock_print:
                command.execute('add')
                df = HistoryManager.get_history_as_df()
                assert df is None, "History should remain empty."
                mock_print.assert_called_with("History is empty")

def test_delete_history_invalid_arguments(setup_test_history):
    '''Test deleting with invalid arguments'''
    command = DeleteHistoryCommand()

    with patch('builtins.print') as mock_print:
        command.execute('multiply', 'invalid_arg')
        df = HistoryManager.get_history_as_df()
        assert len(df) == 4, "History should remain unchanged."
        mock_print.assert_called_with("Invalid argument(s): ('multiply', 'invalid_arg'), please enter command as deletehistory <operation> <optional: operand1 operand2>")
