#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

kill $(ps aux |awk '/main.py/ {print $2}')

cat /dev/null > nohup.out
nohup stdbuf -oL python main.py > nohup.out &

tail -f nohup.out