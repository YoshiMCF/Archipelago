#!/bin/bash

set -e

export PATH="$(pwd)/../venv/bin:$PATH"

mypy
pylint --recursive y worlds/battletech

python WebHost.py
