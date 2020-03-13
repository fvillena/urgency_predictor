#!/bin/sh
echo $(date -u)
cd /usr/wd/urgency_predictor/
python3 download_and_predict.py