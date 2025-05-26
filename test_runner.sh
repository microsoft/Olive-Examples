#!/bin/bash

python -m pip install pytest azure-identity azure-storage-blob tabulate
python -m pytest -v -s --log-cli-level=WARNING --junitxml=~/.pytest_logs/TestExample.xml $1 --basetemp ~/.pytest_basetemp
