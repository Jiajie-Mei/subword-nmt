#!/usr/bin/env bash


target_vocab=vocab_merged.txt

python merge_vocab.py \
--vocab_lcsts ../LCSTS/pg_select/finished_files/vocab \
--vocab_ugc ../UGC/pg_select/finished_files/vocab \
--vocab_merged ${target_vocab}

for data in LCSTS UGC
do
    target_dir=../${data}/pg_select/finished_files
    cp ${target_dir}/vocab ${target_dir}/vocab.bak
    cp ${target_vocab} ${target_dir}/vocab
done
