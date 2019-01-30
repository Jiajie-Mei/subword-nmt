#!/usr/bin/env bash
num_merges=${1}
root_dir=${2}

for data in LCSTS UGC
do
    target_dir=${root_dir}/${data}/subworded_${num_merges}
    mkdir -p ${target_dir}
    for dataset in train val test
    do
        ./subword_nmt/apply_bpe.py -c codec_${num_merges}.txt \
        < ${root_dir}/${data}/pg_select/merged_${dataset}.txt \
        > ${target_dir}/subworded_${dataset}.txt &
    done
done
