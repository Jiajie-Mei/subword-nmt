cp ../LCSTS/pg_select/merged_train.txt train_lcsts.txt
cp ../UGC/pg_select/merged_train.txt train_ugc.txt
cat train_lcsts.txt train_ugc.txt > train_merged.txt
python ./subword_nmt/learn_bpe.py --output_with_freq codec_with_freq.txt  -s 35000 < train_merged.txt > codec.txt
./subword_nmt/get_vocab.py --input train_merged.txt --output vocab.txt
