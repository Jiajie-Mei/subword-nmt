import os
import glob
import sys
import re


dataset = sys.argv[1]

root_dir = 'data/meijiajie/data_processing/'
list_num_merges = [30000, 40000]
list_selective = ['vanilla', 'selective']

target_file = open(os.path.join(root_dir, dataset, 'merged_rouge_results.csv'), 'w')

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

for num_merges in list_num_merges:
    for selective in list_selective:
        list_files = glob.glob(root_dir + dataset + '/subworded_%d/%s/log/mei/decode_test*/ROUGE_results.txt' % (num_merges, selective))
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

        results.insert(0, '%dk,%s' % (num_merges // 1000, selective[:3]))
        target_file.write('\n' + ','.join(results))
