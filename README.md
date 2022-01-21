# avaandmed-py
[![build](https://github.com/Michanix/avaandmed-py/actions/workflows/avaandmed.yml/badge.svg?branch=main)](https://github.com/Michanix/avaandmed-py/actions/workflows/avaandmed.yml)
[![codecov](https://codecov.io/gh/Michanix/avaandmed-py/branch/main/graph/badge.svg?token=DS5MNSZOII)](https://codecov.io/gh/Michanix/avaandmed-py)

## Documentation
- Official [Avaandmed API Swagger](https://avaandmed.eesti.ee/api/dataset-docs/#/)
- Official general [documentation](https://avaandmed.eesti.ee/instructions/api-uldjuhend) about API. Available only in Estonian.

## Requirements
- Python 3.6+

## Installation
## TODO

## Usage
Firstly you going to need to import `avaandmed` package and create client instance. 
Through that you can access necessary information for you Avaandmed account. You can create multiple instances for different accounts as well.

Library trying to copy workflow of API as much as possible.

```python
key_id = 'key_id_value'
token = 'token_value'
client = Avaandmed(api_token=token, key_id=key_id)
```

### Generic datasets
Getting some generic dataset is quite straightforward. Just use `datasets` property provided by `client` instance.

```python
datasets: Datasets = client.datasets
specific_ds: Dataset = datasets.get_by_id(some_ds_id)
```

Getting list of publicly available datasets. By default it will return first 20 datasets, but this can be adjusted by providing `limit` value.

```python
all_datasets: List[Dataset] = client.datasets.get_dataset_list() # retrieve first 20 datasets in the list
get_5_datasets: List[Dataset] = client.datasets.get_dataset_list(limit=5) # retrieves 5 datasets in the list
```

You can apply for access permissions for specific dataset as well. Or submit privacy violations for specific dataset.

```python
client.datasets.apply_for_access('dataset_id', 'description')
client.dataset.file_privacy_violations('dataset_id', 'description')
```


### User's datasets
User's own datasets can be accessed and interacted in the following way.

```python
me: Me = client.users.me
# List all user's dataset
my_dataset: UserDataset = me.dataset

# Retrieves specific dataset
specific_ds: Dataset = me.get_by_id('dataset_id') 
# Delete specific dataset
my_dataset.delete('dataset_id')
# Update dataset
# TODO

# Create dataset
# TODO

# You can consider specific privacy violations for your dataset
my_dataset.consider_privacy_violation('id')

# Or you can discard it
my_dataset.discard_privacy_violation('id')

# Approve access permission by its ID
my_dataset.approve_access_permission('permission_id')

# Decline access permission by its ID
my_dataset.decline_access_permission('permission_id')
```

### Organization's API
Organization's dataset can be accessed and interacted in the similar way as User's.
```python
my_org = client.organization('org_id').my_organization
my_org_ds = my_org.dataset

# List all organizations 
all_orgs = my_org.get_list_my_orgs()

# Retrieve specifc organization
specifc_org = my_org.get_my_org_by_id('org_id')

# Retrieves specific dataset
specific_ds: Dataset = my_org_ds.get_by_id('dataset_id') 
# Delete specific dataset
my_org_ds.delete('dataset_id')
# Update dataset
# TODO

# Create dataset
# TODO

# You can consider specific privacy violations for your dataset
my_org_ds.consider_privacy_violation('id')

# Or you can discard it
my_org_ds.discard_privacy_violation('id')

# Approve access permission by its ID
my_org_ds.approve_access_permission('permission_id')

# Decline access permission by its ID
my_org_ds.decline_access_permission('permission_id')
```


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