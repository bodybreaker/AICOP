#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

kill $(ps aux |awk '/main.py/ {print $2}')

cat /dev/null > nohup.out
nohup python -u main.py &