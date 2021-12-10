from pathlib import Path
from .utils import load_json

DATA_DIR = Path('data')


class DataJsonMock:

    def __init__(self) -> None:
        # Mock data/files
        self.MOCK_DATASET_FILE = load_json(DATA_DIR / 'dataset.json')
        self.MOCK_DATSET_FILE_2 = load_json(DATA_DIR / 'dataset2.json')
        self.MOCK_ERROR_FILE = load_json(DATA_DIR / 'error.json')
        self.MOCK_TOKEN_FILE = load_json(DATA_DIR / 'token.json')
        self.MOCK_DATASET_LIST_FILE = load_json(DATA_DIR / 'dataset_list.json')
        self.MOCK_PREVIEW_FILE = load_json(DATA_DIR / 'preview.json')
        self.MOCK_COLUMNS_FILE = load_json(DATA_DIR / 'file_columns.json')
        self.MOCK_SEARCH_RESULTS = load_json(DATA_DIR / 'search.json')
        self.MOCK_TOKEN_FILE = load_json(DATA_DIR / 'token.json')
