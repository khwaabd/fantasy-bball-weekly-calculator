#!/bin/bash
start=$1
end=$2
year=$3

if [ $# -lt 3 ]
then
    echo "needs start end and year"
    exit 1
fi

echo "starting on week $start and ending on week $end in $year"

for i in $(seq $start $end)
do 
    python3 main.py $i $year > $year-week$i.txt
done 

for i in $(seq $start $end)
do
    echo "Winner for $year $i is"
    tail -n 1 $year-week$i.txt
done

