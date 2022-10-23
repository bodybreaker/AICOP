#!/bin/bash
source /home/itrnd/anaconda3/etc/profile.d/conda.sh
conda activate aicop
cat /dev/null > nohup.out
nohup python main.py &