# avaandmed-py

[![build](https://github.com/Michanix/avaandmed-py/actions/workflows/avaandmed.yml/badge.svg)](https://github.com/Michanix/avaandmed-py/)
[![codecov](https://codecov.io/gh/Michanix/avaandmed-py/branch/main/graph/badge.svg?token=DS5MNSZOII)](https://codecov.io/gh/Michanix/avaandmed-py)

## Documentation
- Official [Avaandmed API Swagger](https://avaandmed.eesti.ee/api/dataset-docs/#/)
- Official general [documentation](https://avaandmed.eesti.ee/instructions/api-uldjuhend) about API. Available only in Estonian.

## Requirements
- Python 3.6+

## Usage
TBD...
or see unit tests in the **tests** folder to get an idea how this library will be used.

## Development
It's recommend to use virtual enviroment during the development.

More information on virtual enviroments can be found [here](https://docs.python.org/3/library/venv.html).

```
git clone https://github.com/Michanix/avaandmed-py.git
cd avaandmed-py
pip install -r requirements.txt
```

### Run tests
[Pytest](https://docs.pytest.org/en/6.2.x/) is used for testing.

[Reponses](https://github.com/getsentry/responses) library is used for mocking responses from Avaadmed API. 

[tox](https://tox.wiki/en/latest/index.html) is used to run tests with different Python versions.

All data for testing is available in **tests/data** folder.

```
cd tests
pytest # to run all tests
pytest path/to/test_file.py # to run specific set of tests
```

Or if you want to use `tox` just run in the root of the folder and it should run tests for all Python versions specified in `tox.ini` file.
However, you probably gonna need to have multiple Python versions on your machine to test with each version. 
Otherwise it will only for tests for version that is currently installed.