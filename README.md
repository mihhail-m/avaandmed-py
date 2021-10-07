# Usage

```python
from avaandmed import Avaandmed
client = Avaandmed(api_token, key_id)
datasets = client.Datasets
dataset1 = datasets.retrieve(dataset_id) # or slug
```