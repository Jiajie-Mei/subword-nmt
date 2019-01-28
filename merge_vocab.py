from __future__ import print_function, division
import io
import os
import argparse
from collections import Counter


def merge(vocab_a, vocab_b, vocab_out):
    new_vocab = vocab_a + vocab_b
    print('add {:.2%} more words to vocab_a'.format(1.0 * len(set(new_vocab) - set(vocab_a)) / len(set(vocab_a))))
    print('add {:.2%} more words to vocab_b'.format(1.0 * len(set(new_vocab) - set(vocab_b)) / len(set(vocab_b))))
    print('#words %d in %s' % (len(set(new_vocab)), vocab_out.name))
    for item in new_vocab.most_common():
        vocab_out.write('%s %d\n' % item)


def load_vocab(obj_vocab_file):
    vocab = Counter()
    for line in obj_vocab_file:
        word, count = line.strip().split()
        vocab.update({word: count})
    print('#words %d in %s' % (len(set(vocab)), obj_vocab_file.name))
    return vocab


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--vocab_lcsts', type=argparse.FileType('r', encoding='utf-8'),
        required=True, metavar='PATH',
        help="path for vocab of lcsts"
    )

    parser.add_argument(
        '--vocab_ugc', type=argparse.FileType('r', encoding='utf-8'),
        required=True, metavar='PATH',
        help="path for vocab of ugc"
    )

    parser.add_argument(
        '--vocab_merged', type=argparse.FileType('w', encoding='utf-8'),
        required=True, metavar='PATH',
        help="path for vocab of ugc"
    )

    args = parser.parse_args()

    merge(load_vocab(args.vocab_lcsts), load_vocab(args.vocab_ugc), args.vocab_merged)
