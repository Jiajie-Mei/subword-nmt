num_merges=${1}

rm -rf train_*
rm -rf codec*
rm -rf vocab*

root_dir=/data/meijiajie/data_processing
train_merged=train_merged.txt

for data in LCSTS UGC
do
    cp ${root_dir}/LCSTS/pg_select/merged_train.txt train_${data}.txt
    cat train_${data}.txt >> ${train_merged}
done

python ./subword_nmt/learn_bpe.py --output_with_freq codec_with_freq_${num_merges}.txt -s ${num_merges} < ${train_merged} > codec_${num_merges}.txt
./subword_nmt/get_vocab.py --input ${train_merged} --output vocab_${num_merges}.txt
python apply.sh ${num_merges} ${root_dir}