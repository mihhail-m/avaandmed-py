from pathlib import Path
from .utils import load_json

DATA_DIR = Path('data')


def load_data_from(filename: str):
    return load_json(DATA_DIR / filename)


class DataJsonMock:

    def __init__(self) -> None:
        # Mock data/files
        self.MOCK_DATASET_FILE = load_data_from('dataset.json')
        self.MOCK_DATSET_FILE_2 = load_data_from('dataset2.json')
        self.MOCK_ERROR_FILE = load_data_from('error.json')
        self.MOCK_TOKEN_FILE = load_data_from('token.json')
        self.MOCK_DATASET_LIST_FILE = load_data_from('dataset_list.json')
        self.MOCK_PREVIEW_FILE = load_data_from('preview.json')
        self.MOCK_COLUMNS_FILE = load_data_from('file_columns.json')
        self.MOCK_SEARCH_RESULTS = load_data_from('search.json')
        self.MOCK_TOKEN_FILE = load_data_from('token.json')
        self.MOCK_PRIVACY_VIOLATIONS = load_data_from(
            'privacy-violations.json')
        self.MOCK_ACCESS_PERMISSIONS = load_data_from('access-perms.json')
        self.MOCK_FILES_LIST = load_data_from('files.json')
        self.MOCK_FILE_INDEX = load_data_from('file_index.json')
        self.MOCK_FILE_PATH = DATA_DIR / 'HighestGrossers.csv'
