#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
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

TOKENIZED_TRAIN = {
    'ashaninka': False,
    'aymara': False,
    'bribri': True,
    'guarani': False,
    'hñähñu': True,
    'nahuatl': True,
    'quechua': False,
    'raramuri': True,
    'shipibo_konibo': False,
    'wixarika': False
}

DEVSETS = ['aymara', 'bribri', 'nahuatl', 'quechua', 'raramuri', 'wixarika']

EXTRA = {
    'aymara': [
        {'prefix': 'parallel_data/es-aym/opus_globalvoices.es-aym'},
        {'prefix': 'extra/sent-boconst_aym'}
    ],
    'hñähñu': [
        {'prefix': 'extra/sent-mxconst'}
    ],
    'nahuatl': [
        {'prefix': 'extra/sent-mxconst'}
    ],
    'quechua': [
        {'prefix': 'dict'},
        {'prefix': 'parallel_data/es-quy/dict_misc.quy-es'},
        {'prefix': 'parallel_data/es-quy/jw300.es-quy'},
        {'prefix': 'parallel_data/es-quy/minedu.quy-es'},
        {'prefix': 'parallel_data/es-quz/jw300.es-quz', 'code': 'quz'},
        {'prefix': 'extra/tatoeba_qu.raw', 'code': 'qu'},
        {'prefix': 'extra/sent-boconst_que', 'code': 'que'},
        {'prefix': 'extra/sent-peconst', 'code': 'que'},
    ],
    'raramuri': [
        {'prefix': 'extra/sent-mxconst'}
    ],
    'shipibo_konibo': [
        {'prefix': 'parallel_data/dictionary'},
        {'prefix': 'parallel_data/educational'},
        {'prefix': 'parallel_data/flashcards'},
        {'prefix': 'extra/Educational_0.4_2.4_35/train-es-shi', 'code': 'shi'},
        {'prefix': 'extra/Educational_0.4_2.4_35/tune-es-shi', 'code': 'shi'},
        {'prefix': 'extra/Educational_0.4_2.4_35/test-es-shi', 'code': 'shi'},
        {'prefix': 'extra/Religious_0.2_2.4_35/train-es-shi', 'code': 'shi'},
        {'prefix': 'extra/Religious_0.2_2.4_35/tune-es-shi', 'code': 'shi'},
        {'prefix': 'extra/Religious_0.2_2.4_35/test-es-shi', 'code': 'shi'},
    ],
    'wixarika': [
        {'prefix': 'extra/sent-mxconst'},
        {'prefix': 'extra/corp-train', 'code': 'wix'},
        {'prefix': 'extra/corp-dev', 'code': 'wix'},
        {'prefix': 'extra/corp-test', 'code': 'wix'}
    ]
}

BIBLES = {
    'ashaninka': ['cni-x-bible-cni-v1.txt'],
    'aymara': ['ayr-x-bible-1997-v1.txt', 'ayr-x-bible-2011-v1.txt'],
    'bribri': ['bzd-x-bible-bzd-v1.txt'],
    'guarani': ['gug-x-bible-gug-v1.txt'],
    'hñähñu': ['ote-x-bible-ote-v1.txt'],
    'nahuatl': [
        'nah-NHXNTV.txt',
        'azz-x-bible-azz-v1.txt',
        'nch-x-bible-nch-v1.txt',
        'ncj-x-bible-ncj-v1.txt',
        'ngu-x-bible-ngu-v1.txt',
        'nhe-x-bible-nhe-v1.txt',
        'nhi-x-bible-nhi-v1.txt',
        'nhw-x-bible-nhw-v1.txt',
        'nhy-x-bible-nhy-v1.txt'
    ],
    'quechua': ['quy-x-bible-quy-v1.txt', 'quz-x-bible-quz-v1.txt'],
    'raramuri': ['tac-x-bible-tac-v1.txt'],
    'shipibo_konibo': ['shp-SHPTBL.txt'],
    'wixarika': ['hch-x-bible-hch-v1.txt'],
    'spanish': [
        'spa-x-bible-americas.txt.jhubc',
        'spa-x-bible-hablahoi-latina.txt.jhubc',
        'spa-x-bible-lapalabra.txt.jhubc',
        'spa-x-bible-newworld.txt.jhubc',
        'spa-x-bible-nuevadehoi.txt.jhubc',
        'spa-x-bible-nuevaviviente.txt.jhubc',
        'spa-x-bible-nuevointernacional.txt.jhubc',
        'spa-x-bible-reinavaleracontemporanea.txt.jhubc'
    ]
}


def get_bible_files(lang):
    return ['../data/bibles/{lang}/{fname}'.format(lang=lang, fname=fname) for fname in BIBLES[lang]]


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

    # Detokenize train sets
    for lang in LANGUAGES:
        if not TOKENIZED_TRAIN[lang]:
            continue
        inputs = get_input_files(lang)  # train.lang
        outputs = get_work_files(lang, 'train')
        steps.append({
            'type': 'preprocess',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'preprocessors': [
                    {'Detokenizer': {
                        'tokenizer': 'moses',
                        'languages': ['es', LANGCODE[lang]]
                    }}
                ]
            }
        })

    # Bibles
    for lang in LANGUAGES:
        inputs = [get_bible_files('spanish'), get_bible_files(lang)]
        outputs = get_work_files(lang, 'bibles')
        steps.append({
            'type': 'product',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'skip_empty': True,
                'skip_duplicates': True,
                'k': 10,
                'seed': 'bibles'
            }
        })

    # TODO: add extra cleaning for specific corpora?
    # * the wixarika bible should use normalization in normwix.py

    # Combine training data sets
    for lang in LANGUAGES:
        if TOKENIZED_TRAIN[lang]:
            inputs = [get_work_files(lang, 'train')]
        else:
            inputs = [get_input_files(lang)]
        inputs.append(get_work_files(lang, 'bibles'))
        if lang in EXTRA:
            for params in EXTRA[lang]:
                inputs.append(get_input_files(lang, **params))
        for idx in [0, 1]:
            steps.append({
                'type': 'concatenate',
                'parameters': {
                    'inputs': [f[idx] for f in inputs],
                    'output': get_work_files(lang, 'combined')[idx]
                }
            })

    # Normalize whitespaces
    for lang in LANGUAGES:
        inputs = get_work_files(lang, 'combined')
        outputs = get_work_files(lang, 'input')
        steps.append({
            'type': 'preprocess',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'preprocessors': [{'WhitespaceNormalizer': {}}]
            }
        })

    # Remove duplicates
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

    # Tokenize training sets
    # FIXME: does not work properly at least for wixarika
    for lang in LANGUAGES:
        inputs = get_work_files(lang, 'dedup_filtered')
        outputs = get_work_files(lang, 'dedup_filtered_tokenized')
        steps.append({
            'type': 'preprocess',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'preprocessors': [
                    {'Tokenizer': {
                        'tokenizer': 'moses',
                        'languages': ['es', LANGCODE[lang]]
                    }}
                ]
            }
        })

    # Tokenize dev sets
    for lang in DEVSETS:
        inputs = get_input_files(lang, prefix='dev')
        outputs = get_work_files(lang, prefix='dev_tokenized')
        steps.append({
            'type': 'preprocess',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'preprocessors': [
                    {'Tokenizer': {
                        'tokenizer': 'moses',
                        'languages': ['es', LANGCODE[lang]]
                    }}
                ]
            }
        })

    logging.info("%s steps generated for %s", len(steps), output)

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
    logging.basicConfig(level=logging.INFO)
    main(args.output, args.workdir)
