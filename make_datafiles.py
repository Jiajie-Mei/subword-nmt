from __future__ import print_function
import io
import os
import sys
import tensorflow as tf
import pandas as pd
import struct
import collections


# We use these to separate the summary sentences in the .bin datafiles
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'

root_dir = sys.argv[1]
finished_files_dir = os.path.join(root_dir, "finished_files")
chunks_dir = os.path.join(finished_files_dir, "chunked")

sep_general = '\t'


VOCAB_SIZE = 200000
CHUNK_SIZE = 1000  # num examples per chunk, for the chunked data


def chunk_file(set_name):
    in_file = os.path.join(finished_files_dir, '%s.bin' % set_name)
    reader = open(in_file, "rb")
    chunk = 0
    finished = False
    while not finished:
        chunk_fname = os.path.join(chunks_dir, '%s_%03d.bin' % (set_name, chunk)) # new chunk
        with open(chunk_fname, 'wb') as writer:
            for _ in range(CHUNK_SIZE):
                len_bytes = reader.read(8)
                if not len_bytes:
                    finished = True
                    break
                str_len = struct.unpack('q', len_bytes)[0]
                example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
                writer.write(struct.pack('q', str_len))
                writer.write(struct.pack('%ds' % str_len, example_str))
            chunk += 1


def chunk_all():
    # Make a dir to hold the chunks
    if not os.path.isdir(chunks_dir):
        os.mkdir(chunks_dir)
    # Chunk the data
    for set_name in ['train', 'val', 'test']:
        print("Splitting %s data into chunks..." % set_name)
        chunk_file(set_name)
    print("Saved chunked data in %s" % chunks_dir)


def write_to_bin(list_sum_art, out_file, make_vocab=False):
    print("Making bin file for summary-article pairs")

    vocab_counter = collections.Counter()

    num_pairs = len(list_sum_art)
    with open(out_file, 'wb') as writer:
        for idx, sum_art in enumerate(list_sum_art):
            if idx % 1000 == 0:
                print("Writing pair %i/%i; %.2f percent done" % (idx, num_pairs, idx * 100 / num_pairs))

            # Get the strings to write to .bin file
            shop, abstract, article = sum_art

            # Write to tf.Example
            feature_shop = tf.train.Feature(bytes_list=tf.train.BytesList(value=[shop.encode()]))
            feature_art = tf.train.Feature(bytes_list=tf.train.BytesList(value=[article.encode()]))
            feature_sum = tf.train.Feature(bytes_list=tf.train.BytesList(value=[abstract.encode()]))
            example_proto = tf.train.Example(features=tf.train.Features(feature={
                'shop': feature_shop,
                'abstract': feature_sum,
                'article': feature_art
            }))

            tf_example_str = example_proto.SerializeToString()
            str_len = len(tf_example_str)

            writer.write(struct.pack('q', str_len))
            writer.write(struct.pack('%ds' % str_len, tf_example_str))

            # Write the vocab to file, if applicable
            if make_vocab:
                art_tokens = article.split(' ')
                abs_tokens = abstract.split(' ')
                abs_tokens = [t for t in abs_tokens if t not in [SENTENCE_START, SENTENCE_END]]
                tokens = art_tokens + abs_tokens
                tokens = [t.strip() for t in tokens]  # strip
                tokens = [t for t in tokens if t != '']  # remove empty
                vocab_counter.update(tokens)

    print("Finished writing file %s\n" % out_file)

    # write vocab to file
    if make_vocab:
        print("Writing vocab file...")
        with open(os.path.join(finished_files_dir, "vocab"), 'w') as writer:
            for word, count in vocab_counter.most_common():
                writer.write(word + ' ' + str(count) + '\n')
        print("Finished writing vocab file")


def load_file(dataset):
    shops = pd.read_csv(os.path.join(root_dir, 'shops_%s.txt' % dataset), header=None, names=['poi'], dtype=str)['poi'].values.tolist()

    with io.open(os.path.join(root_dir, 'subworded_%s.txt' % dataset), 'r', encoding='utf-8') as f:
        arts_and_sums = [line.strip() for line in f.readlines() if len(line.strip()) != 0]

    arts = arts_and_sums[0::2]
    sums = arts_and_sums[1::2]

    try:
        assert len(shops) == len(arts) == len(sums)
    except AssertionError:
        print(len(shops), len(arts), len(sums))
        exit(0)

    return [tuple([x[0], '%s %s %s' % (SENTENCE_START, x[1], SENTENCE_END), x[2]]) for x in zip(shops, sums, arts)]


def convert_subword2tfexample():

    if os.path.exists(finished_files_dir):
        os.rename(finished_files_dir, 'non_subworded_finished_files')

    if not os.path.exists(chunks_dir):
        os.makedirs(chunks_dir)

    for dataset in ['test', 'val', 'train']:
        data = load_file(dataset)
        for item in data[0]:
            print(item)
        write_to_bin(data, os.path.join(finished_files_dir, "%s.bin" % dataset), make_vocab=dataset == 'train')

    """
    Chunk the data. This splits each of train.bin, val.bin and test.bin into smaller chunks, 
    each containing e.g. 1000 examples, and saves them in finished_files/chunks

    """
    chunk_all()


def prepare_original(data_type):
    lines = []
    shops = []
    with open('finished_files/%s.bin' % data_type, 'rb') as f:
        while True:
            len_bytes = f.read(8)
            if not len_bytes:
                break
            str_len = struct.unpack('q', len_bytes)[0]
            example_str = struct.unpack('%ds' % str_len, f.read(str_len))[0]
            e = tf.train.Example.FromString(example_str)
            shop = e.features.feature['shop'].bytes_list.value[0]
            article_text = e.features.feature['article'].bytes_list.value[0]  # the article text was saved under the key 'article' in the data files
            abstract_text = e.features.feature['abstract'].bytes_list.value[0]
            lines.append(article_text.strip())
            lines.append(abstract_text.strip('<s>').strip('</s>').strip())
            shops.append(shop)

    with io.open('merged_%s.txt' % data_type, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines).decode('utf-8'))
    with io.open('shops_%s.txt' % data_type, 'w', encoding='utf-8') as f:
        f.write('\n'.join(shops).decode('utf-8'))


if __name__ == '__main__':

    # op = sys.argv[1]

    # if op == 'prepare':
    #     for data_type_ in ['train', 'val', 'test']:
    #         prepare_original(data_type_)
    # elif op == 'convert':
    convert_subword2tfexample()
