#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

kill $(pgrep -f 'python main.py')

cat /dev/null > nohup.out
nohup python main.py &

tail -f nohup.out