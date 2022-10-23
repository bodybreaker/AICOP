#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop

cat /dev/null > nohup.out

kill -9 `netstat -tnlp|grep 6789|gawk '{ print $7 }'|grep -o '[0-9]*'`

nohup python main.py &