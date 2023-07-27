# Contributing

Contributions are welcome, please follow the setup instructions below to get started.

## Setup

### Clone the repository

```bash
git clone https://github.com/torchbox/wagtail-jotform
```

### Create a virtual environment and install the requirements

```bash
cd wagtail-jotform
python3 -m venv venv
source venv/bin/activate
pip install -e ".[testing,development]"
```

### Install the pre-commit hooks

```bash
pre-commit install
```

### Do some work, write some tests

Change some code, write some tests, and check that the tests pass

### Run the tests

```bash
coverage run ./runtests.py
coverage report
```
