import argparse
import collections
import gzip
import logging
import os

from tabulate import tabulate

from create_opusfilter_config import LANGUAGES, LANGCODE, get_work_files


def get_num_lines(fname):
    with gzip.open(fname, 'r') as fobj:
        num_lines = sum(1 for line in fobj)
    return num_lines


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('workdir', type=str, help='OpusFilter work directory')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    
    prefixes = ['train', 'extra', 'combined', 'dedup', 'dedup_filtered', 'bibles', 'monolingual', 'dev']

    table = {}
    table['language'] = [l.replace('_', '-').title() for l in LANGUAGES]
    table['code'] = [LANGCODE[l] for l in LANGUAGES]
    for prefix in prefixes:
        row = []
        for lang in LANGUAGES:
            src, tgt = get_work_files(lang, prefix)
            fname = os.path.join(args.workdir, tgt)
            if os.path.isfile(fname):
                lines = get_num_lines(fname)
            else:
                lines = 0
            row.append(lines)
            logging.info("%s %s", fname, lines)
        if prefix == 'dedup_filtered':
            label = 'filtered'
        else:
            label = prefix
        table[label] = row

    print(tabulate(table, headers=table.keys(), tablefmt='latex'))
