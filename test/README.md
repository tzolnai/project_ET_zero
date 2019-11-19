### Testing

To run all tests:
- Install pytest: pip install pytest
- Run this command from \test folder: `pytest`

To check test coverage:
- Download pytest-cov: https://pypi.org/project/pytest-cov/
- Run this command from \test folder: `pytest --cov=asrt`

To check uncovered lines:
- Run this command: `pytest --cov-report term-missing --cov=asrt`
