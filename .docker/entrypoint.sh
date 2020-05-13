#!/bin/sh
envsubst < .env.tpl > .env
python3 main.py