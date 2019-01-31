#!/usr/bin/env bash

num_merges=${1}
#target_dir=${2}

target_vocab=vocab_merged.txt
root_dir=/data/meijiajie/data_processing


python merge_vocab.py \
--vocab_lcsts ${root_dir}/LCSTS/subworded_${num_merges}/finished_files/vocab \
--vocab_ugc ${root_dir}/UGC/subworded_${num_merges}/finished_files/vocab \
--vocab_merged ${target_vocab}

for data in LCSTS UGC
do
    target_dir=${root_dir}/${data}/subworded_${num_merges}/finished_files
    cp ${target_dir}/vocab ${target_dir}/vocab.bak
    cp ${target_vocab} ${target_dir}/vocab
done
