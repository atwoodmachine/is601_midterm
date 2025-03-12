'''Test clear history'''
import os
import tempfile
from unittest.mock import patch
import pytest
import pandas as pd
from calculator.historyManager import HistoryManager
from calculator.plugins.clearhistory import ClearHistoryCommand

@pytest.fixture
def mock_history_data():
    '''Create a temporary directory for testing'''
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

def test_clear_history_command(mock_history_data):
    '''Test history is cleared'''
    df_before = pd.read_csv(HistoryManager.get_history_path())
    assert not df_before.empty, "History file should not be empty before clearing."

    with patch('builtins.print') as mock_print:
        command = ClearHistoryCommand()
        command.execute()

        df_after = pd.read_csv(HistoryManager.get_history_path())
        assert df_after.empty, "History file should be empty after clearing."
        mock_print.assert_called_with("Calculation history cleared.")
