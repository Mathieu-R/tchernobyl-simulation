#!/usr/bin/env bash

python3 -m venv env
/bin/bash -c "source ./env/bin/activate"
pip3 install --upgrade pip
pip3 install matplotlib numpy PyInquirer ttkthemes