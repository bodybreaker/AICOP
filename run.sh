#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

cat /dev/null > nohup.out

kill -9 $(ps -ef | grep main.py | head -1 | awk '{print $2}')

nohup python main.py &
tail -f nohup.out