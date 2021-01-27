#!/bin/bash
#
python modeling/main.py -W $1 -C $2 -L $3 -P $4 -OUT $5 -D unit -D cycles -F $6 -O True
echo "done"