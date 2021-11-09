# avaandmed-py

## Documentation
- Official [Avaandmed API Swagger](https://avaandmed.eesti.ee/api/dataset-docs/#/)
- Official general [documentation](https://avaandmed.eesti.ee/instructions/api-uldjuhend) about API. Available only in Estonian.

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

All data for testing is available in **tests/data** folder.

```
cd tests
pytest # to run all tests
pytest path/to/test_file.py # to run specific set of tests
```