'''Test class HistoryManager'''
import os
from unittest.mock import patch
import pytest
import pandas as pd
from calculator.historyManager import HistoryManager

@pytest.fixture
def setup_history_manager():
    '''Sets up mock directory and tears it down after testing'''
    if not os.path.exists(HistoryManager.HISTORY_DIR):
        os.makedirs(HistoryManager.HISTORY_DIR)
    yield

    if os.path.exists(HistoryManager.HISTORY_DIR):
        for file in os.listdir(HistoryManager.HISTORY_DIR):
            os.remove(os.path.join(HistoryManager.HISTORY_DIR, file))
        os.rmdir(HistoryManager.HISTORY_DIR)

def test_initialize_history_creates_directory():
    '''Test directory is created if not exists'''
    if os.path.exists(HistoryManager.HISTORY_DIR):
        for file in os.listdir(HistoryManager.HISTORY_DIR):
            os.remove(os.path.join(HistoryManager.HISTORY_DIR, file))
        os.rmdir(HistoryManager.HISTORY_DIR)

    HistoryManager.initialize_history()
    assert os.path.exists(HistoryManager.HISTORY_DIR), "History directory was not created."


def test_initialize_history_non_writable_directory(setup_history_manager):
    '''Test for non-writable directory'''
    os.chmod(HistoryManager.HISTORY_DIR, 0o444)
    with patch('logging.error') as e:
        HistoryManager.initialize_history()
        e.assert_called_with(f"The directory {HistoryManager.HISTORY_DIR} is not writeable")

def test_add_to_history_creates_file(setup_history_manager):
    '''Test that a new file is created if the history file doesn't exist'''
    command_name = 'add'
    args = [1.0, 2.0]
    result = 3
    HistoryManager.add_to_history(command_name, args, result)

    csv_file_path = os.path.join(HistoryManager.HISTORY_DIR, HistoryManager.HISTORY_FILE)
    assert os.path.exists(csv_file_path), "History file was not created."

    df = pd.read_csv(csv_file_path)
    assert not df.empty, "History file is empty."
    assert df['Operation'][0] == command_name, "Operation not correctly added."
    assert df['Arguments'][0] == str(args), "Arguments not correctly added."
    assert df['Result'][0] == result, "Result not correctly added."

def test_add_to_history_appends_to_file(setup_history_manager):
    '''Test that data is appended to the history file if it exists'''
    command_name1 = 'add'
    args1 = [1, 2]
    result1 = 3
    HistoryManager.add_to_history(command_name1, args1, result1)

    command_name2 = 'subtract'
    args2 = [5, 2]
    result2 = 3
    HistoryManager.add_to_history(command_name2, args2, result2)

    csv_file_path = os.path.join(HistoryManager.HISTORY_DIR, HistoryManager.HISTORY_FILE)
    df = pd.read_csv(csv_file_path)

    assert len(df) == 2, "History file does not have the correct number of entries."
    assert df['Operation'][1] == command_name2, "Second operation not correctly added."

def test_get_history_as_df(setup_history_manager):
    '''Test that get_history_as_df returns a DataFrame when the file exists'''
    command_name = 'add'
    args = [1, 2]
    result = 3
    HistoryManager.add_to_history(command_name, args, result)

    df_history = HistoryManager.get_history_as_df()
    assert isinstance(df_history, pd.DataFrame), "Returned object is not a DataFrame."
    assert not df_history.empty, "Returned DataFrame is empty."

def test_get_history_as_df_file_not_found(setup_history_manager):
    '''Test that get_history_as_df returns None if the file doesn't exist'''
    csv_file_path = os.path.join(HistoryManager.HISTORY_DIR, HistoryManager.HISTORY_FILE)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    df_history = HistoryManager.get_history_as_df()
    assert df_history is None, "Expected None when history file doesn't exist."

def test_get_history_path():
    '''Test get_history_path returns correct path'''
    expected_path = os.path.join(HistoryManager.HISTORY_DIR, HistoryManager.HISTORY_FILE)
    assert HistoryManager.get_history_path() == expected_path, "History path is incorrect."
