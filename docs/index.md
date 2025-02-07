# RADEX Docs

Demo searches
```python
from radex import Radex

radex = Radex()
radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
radex.preprocess_data()

radex.run_example_searches()
radex.save_output('output.csv')
```

With custom searches
```python
from radex import Radex

radex = Radex()
radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
radex.preprocess_data()

radex.searches = {'thyroid nodule': 'thyr* NEAR2 nodul*'} # custom search-name: searches
radex.run_searches()
radex.save_output('output.csv')
```


