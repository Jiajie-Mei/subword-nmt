#!/usr/bin/env bash
num_merges=${1}
root_dir=/data/meijiajie/data_processing

for data in LCSTS UGC
do
    target_dir=${root_dir}/${data}/subworded_${num_merges}
    mkdir -p ${target_dir}
    for dataset in train val test
    do
        ./subword_nmt/apply_bpe.py -c codec_${num_merges}.txt \
        < ${root_dir}/${data}/original_data/merged_${dataset}.txt \
        > ${target_dir}/subworded_${dataset}.txt
        cp ${root_dir}/${data}/original_data/shops_${dataset}.txt ${target_dir}
    done
    python make_datafiles.py ${target_dir}
done

bash merge_vocab.sh ${num_merges}