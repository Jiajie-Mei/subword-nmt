import os
import glob
import sys
import re


root_dir = sys.argv[1]

list_selective = ['noselective', 'selective']

target_file = open(os.path.join(root_dir, 'merged_rouge_results.csv'), 'w')

list_str_metric = ['precision', 'recall', 'f_score']
list_ngram = ['1', '2', 'l']

header = ['\\']
item2id = dict()
counter = 0
for str_metric in list_str_metric:
    for ngram in list_ngram:
        header.append('ROUGE-%s-%s' % (str_metric, ngram))
        item2id[str_metric+ngram] = counter
        counter += 1

target_file.write(','.join(header))

pattern = r'rouge_(\w)_(.*?): (\d+\.\d+)'

possible_dir = ['rnn_baseline', 'no_query', 'query_in_encoder', 'query_in_decoder', 'query_in_both']

for dir_ in possible_dir:
    if not os.path.exists(os.path.join(root_dir, dir_)):
        continue
    for selective in list_selective:
        list_files = glob.glob(root_dir + '/%s' % dir + '/%s/log/mei/decode_test*/ROUGE_results.txt' % selective)
        results = ['-'] * (len(list_str_metric) * len(list_ngram))
        if len(list_files) == 0:
            pass
        else:
            try:
                assert len(list_files) == 1
            except AssertionError:
                print(list_files)
                exit(0)
            single_line = ' '.join([line.strip() for line in open(list_files[0], 'r').readlines()])
            for ngram, str_metric, str_value in re.findall(pattern, single_line):
                results[item2id[str_metric+ngram]] = str_value

        results.insert(0, '%s_%s' % (dir_, selective))
        target_file.write('\n' + ','.join(results))
