#!/bin/bash

ts_from="$(date --date="1 hour ago" +"%Y-%m-%d %H:%M")"
ts_to="$(date +"%Y-%m-%d %H:%M")"

python submit_jobs.py "\"$ts_from\"" "\"$ts_to\"" bai_pred_config.json