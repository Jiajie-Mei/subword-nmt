#!/usr/bin/env bash
num_merges=${1}

rm -rf train_*
rm -rf codec*
rm -rf vocab*

root_dir=/data/meijiajie/data_processing
train_merged=train_merged_${num_merges}.txt

for data in LCSTS UGC
do
    cat ${root_dir}/LCSTS/original_data/merged_train.txt >> ${train_merged}
done

python ./subword_nmt/learn_bpe.py --output_with_freq codec_with_freq_${num_merges}.txt -s ${num_merges} < ${train_merged} > codec_${num_merges}.txt
./subword_nmt/get_vocab.py --input ${train_merged} --output vocab_${num_merges}.txt
bash apply.sh ${num_merges}