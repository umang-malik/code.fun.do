#!/bin/bash

output_list=$(ls -U summary/ | head -6)
rm -rf output/
mkdir output/
i=1
for f in $output_list; do 
    echo $f >| "output/tweet$i.txt"
    cat "summary/$f" >| "output/tweet${i}_summary.txt"
    i=$(($i+1))
done
rm -rf final/site/output
cp -r output final/site/output