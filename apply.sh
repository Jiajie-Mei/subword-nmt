#!/usr/bin/env bash

for data in LCSTS UGC
do
    for dataset in train val test
    do
        ./subword_nmt/apply_bpe.py -c codec.txt \
        < ../${data}/pg_select/merged_${dataset}.txt \
        > ../${data}/pg_select/subworded_${dataset}.txt &
    done
done
