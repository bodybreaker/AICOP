#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

kill $(ps aux |awk '/main.py/ {print $2}')

cat /dev/null > nohup.out
nohup python main.py > log.output 2>&1 &

tail -f nohup.out