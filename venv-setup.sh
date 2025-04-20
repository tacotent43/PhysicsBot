#!/bin/bash

if ! command -v python3 &> /dev/null; then
  echo "Python3 is not installed. Please install Python3 and try again."
  exit 1
fi

python3 -m venv .venv

source .venv/bin/activate

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
  echo "Dependencies installed."
else
  echo "File requirements.txt not found. Packages not installed."
fi