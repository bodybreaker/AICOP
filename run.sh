#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

kill -9 $(ps aux |awk '/main.py/ {print $2}')

nohup python main.py &

tail -f nohup.out