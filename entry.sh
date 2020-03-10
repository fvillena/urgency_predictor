#!/bin/sh
service cron start
python3 download_and_predict.py
python3 app.py 