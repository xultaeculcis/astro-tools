This page describes how to run tests locally using `pytest`.

## Instructions

To run tests marked as `unit` tests:

````shell
pytest -m "unit" -v

To run all tests:

```shell
pytest
````

???+ note

    Pre-commit hooks will only run those tests marked as `unit`.
