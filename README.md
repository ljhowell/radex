

---
# RADEX: a rule-based clinical and radiology data extraction tool 

<!-- bubbles for tests and citation etc -->
[![codecov](https://codecov.io/gh/ljhowell/radex/branch/main/graph/badge.svg?token=radex_token_here)](https://codecov.io/gh/ljhowell/radex)
[![CI](https://github.com/ljhowell/radex/actions/workflows/main.yml/badge.svg)](https://github.com/ljhowell/radex/actions/workflows/main.yml)

<!-- TOC -->
![TOC_new](https://github.com/user-attachments/assets/fe28f78e-81fe-4cc9-b282-2b28525f01ca)

Clincal reports contain valuable information for research and audits, but relevant details are often buried within free-text fields. The RAdiology Data EXtraction tool (RADEX) was designed as a simple and practical interface for information extraction in clinical documents, enabling context-dependent searching without specialist expertise in Natural Language Processing. 

RADEX relies on a user-friendly 'search strategy' which is defined and refined to classify reports and extract information for research and audit. In the code backend, the search strategy is converted to a regular expression model which is applied to the dataset. 

**If you use this software, please cite our paper: Howell et al. (2025). European Radiology. [https://doi.org/10.1007/s00330-025-11416-4](https://doi.org/10.1007/s00330-025-11416-4)**

---
# Getting started

## Installation


## Install it from PyPI

```bash
pip install radex
```

## Usage

```py
from radex import BaseClass
from radex import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m radex
#or
$ radex
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
