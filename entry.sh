#!/bin/sh
service cron start
python3 /usr/wd/urgency_predictor/download_and_predict.py
python3 /usr/wd/urgency_predictor/app.py 