#!/bin/bash

set -e

export PATH="$(pwd)/../venv/bin:$PATH"

set -x

mypy
pylint --recursive y worlds/battletech

python WebHost.py
