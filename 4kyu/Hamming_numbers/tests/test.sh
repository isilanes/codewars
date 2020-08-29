python -m coverage run --source="." -m unittest discover -s tests -v --failfast

flake8
find . -name "*.py" -exec radon cc -nc {} +
find . -name "*.py" -exec radon mi -nb {} +

python -m coverage report -m --skip-covered
