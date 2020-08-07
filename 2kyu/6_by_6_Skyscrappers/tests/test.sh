python -m coverage run --source="." -m unittest discover -s tests -v --failfast
python -m coverage report -m --skip-covered
