#!/bin/bash

rm -rf ./include/nagisa
mkdir ./include/nagisa
python ./tools/create_link/main.py ./include/nagisa ./submodules
