#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os

from yaml import dump, Dumper


LANGUAGES = ['ashaninka', 'aymara', 'bribri', 'guarani', 'hñähñu', 'nahuatl', 'quechua', 'raramuri', 'shipibo_konibo', 'wixarika']

LANGCODE = {
    'ashaninka': 'cni',
    'aymara': 'aym',
    'bribri': 'bzd',
    'guarani': 'gn',  
    'hñähñu': 'oto',
    'nahuatl': 'nah',
    'quechua': 'quy',
    'raramuri': 'tar',
    'shipibo_konibo': 'shp',
    'wixarika': 'hch'
}

DEVSETS = ['aymara', 'bribri', 'nahuatl', 'quechua', 'raramuri', 'wixarika']

EXTRA = {
    'quechua': [
        {'prefix': 'dict'},
        {'prefix': 'parallel_data/es-quy/dict_misc.quy-es'},
        {'prefix': 'parallel_data/es-quy/jw300.es-quy'},
        {'prefix': 'parallel_data/es-quy/minedu.quy-es'},
        {'prefix': 'parallel_data/es-quz/jw300.es-quz', 'code': 'quz'},
    ],
    'aymara': [
        {'prefix': 'parallel_data/es-aym/opus_globalvoices.es-aym'}
    ],
    'shipibo_konibo': [
        {'prefix': 'parallel_data/dictionary'},
        {'prefix': 'parallel_data/educational'},
        {'prefix': 'parallel_data/flashcards'},
    ]
}


def get_input_files(lang, prefix='train', code=None):
    src = '../data/{lang}-spanish/{prefix}.es'.format(lang=lang, prefix=prefix)
    tgt = '../data/{lang}-spanish/{prefix}.{code}'.format(
        lang=lang, prefix=prefix, code=LANGCODE[lang] if code is None else code)
    return [src, tgt]


def get_work_files(lang, prefix):
    code = LANGCODE[lang]
    src = '{lang}/{prefix}.es.gz'.format(
        code=code, lang=lang, prefix=prefix)
    tgt = '{lang}/{prefix}.{code}.gz'.format(
        code=code, lang=lang, prefix=prefix)
    return [src, tgt]



def main(output, workdir):
    # WORKDIR = 'processed_data'
    # OUTPUT = 'opusfilter.yaml'

    steps = []

    # Copy dev sets
    for lang in DEVSETS:
        for idx in [0, 1]:
            steps.append({
                'type': 'concatenate',
                'parameters': {
                    'inputs': [get_input_files(lang, prefix='dev')[idx]],
                    'output': get_work_files(lang, prefix='dev')[idx]
                }
            })

    # Combine training data sets
    for lang in LANGUAGES:
        inputs = [get_input_files(lang)]  # train.lang
        if lang in EXTRA:
            for params in EXTRA[lang]:
                inputs.append(get_input_files(lang, **params))
        for idx in [0, 1]:
            steps.append({
                'type': 'concatenate',
                'parameters': {
                    #'inputs': [get_input_files('quechua', code='quz')[idx],
                    #           get_input_files('quechua', prefix='dict')[idx]],
                    'inputs': [f[idx] for f in inputs],
                    'output': get_work_files(lang, 'input')[idx]
                }
            })

    # remove duplicates
    for lang in LANGUAGES:
        inputs = get_work_files(lang, 'input')
        steps.append({
            'type': 'remove_duplicates',
            'parameters': {
                'inputs': inputs,
                'outputs': get_work_files(lang, 'dedup')
            }
        })

    filter_params = {
        'LengthFilter': {'unit': 'char', 'min_length': 1, 'max_length': 1000},
        'LengthRatioFilter': {'unit': 'char', 'threshold': 4},
        'CharacterScoreFilter': {'scripts': ['Latin', 'Latin'], 'thresholds': [0.9, 0.9]},
        'TerminalPunctuationFilter': {'threshold': -2},
        'NonZeroNumeralsFilter': {'threshold': 0.5}
    }
    
    active_filters = {
        'ashaninka': ['LengthRatioFilter'],
        'aymara': ['LengthFilter', 'LengthRatioFilter', 'CharacterScoreFilter',
                   'TerminalPunctuationFilter', 'NonZeroNumeralsFilter'],
        'bribri': [],
        'guarani': ['LengthRatioFilter'],
        'hñähñu': ['LengthRatioFilter'],
        'nahuatl': ['LengthFilter', 'LengthRatioFilter'],
        'quechua': ['LengthFilter', 'LengthRatioFilter', 'CharacterScoreFilter',
                    'TerminalPunctuationFilter', 'NonZeroNumeralsFilter'],
        'raramuri': ['LengthFilter', 'LengthRatioFilter', 'CharacterScoreFilter',
                     'NonZeroNumeralsFilter'],
        'shipibo_konibo': [],
        'wixarika': ['LengthRatioFilter', 'NonZeroNumeralsFilter']
    }
    
    for lang in LANGUAGES:
        inputs = get_work_files(lang, 'dedup')
        outputs = get_work_files(lang, 'dedup_filtered')
        filters = [{filt: filter_params[filt]} for filt in active_filters[lang]]
        steps.append({
            'type': 'filter',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'filters': filters
            }
        })

    # Write YAML configuration for opusfilter
    config = {
        'common': {
            'output_directory': workdir
        },
        'steps': steps
    }
    with open(output, 'w') as fobj:
        fobj.write(dump(config, Dumper=Dumper))

    # create lang subdirs (TODO: fix OpusFilter to be able to create new input dirs)
    os.makedirs(workdir, exist_ok=True)
    for lang in LANGUAGES:
        os.makedirs(os.path.join(workdir, lang), exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create OpusFilter configuration')
    parser.add_argument('output', metavar='FILE', help='OpusFilter config file')
    parser.add_argument('workdir', metavar='DIR', help='Work directory for OpusFilter')
    args = parser.parse_args()
    main(args.output, args.workdir)
