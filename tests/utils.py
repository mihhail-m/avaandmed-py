import json
from pathlib import Path


def load_json(path: Path):
    data = None
    with open(path.absolute(), encoding='utf-8') as f:
        data = json.load(f)
    return data


def format_mock_url(url: str, mock_value: str):
    return f'{url}{mock_value}'
