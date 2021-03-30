#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import copy
import logging
import os
import re

import opusfilter
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
        {'prefix': 'extra/corpora', 'code': 'wix'},
        {'prefix': 'extra/paral_own', 'code': 'wix'},
        {'prefix': 'extra/segcorpus', 'code': 'wix'},
        # Note: train.wix/hch is the combination of these:
        # {'prefix': 'extra/corp-train', 'code': 'wix'},
        # {'prefix': 'extra/corp-dev', 'code': 'wix'},
        # {'prefix': 'extra/corp-test', 'code': 'wix'}
    ]
}

# Only parallel datasets provided by the organizers
RESTRICTED_EXTRA = {
    'aymara': [
        {'prefix': 'parallel_data/es-aym/opus_globalvoices.es-aym'}
    ],
    'quechua': [
        {'prefix': 'dict'},
        {'prefix': 'parallel_data/es-quy/dict_misc.quy-es'},
        {'prefix': 'parallel_data/es-quy/jw300.es-quy'},
        {'prefix': 'parallel_data/es-quy/minedu.quy-es'},
        {'prefix': 'parallel_data/es-quz/jw300.es-quz', 'code': 'quz'},
    ],
    'shipibo_konibo': [
        {'prefix': 'parallel_data/dictionary'},
        {'prefix': 'parallel_data/educational'},
        {'prefix': 'parallel_data/flashcards'},
    ]
}

BIBLES = {
    'ashaninka': ['cni-x-bible-cni-v1.txt'],
    'aymara': ['ayr-x-bible-1997-v1.txt', 'ayr-x-bible-2011-v1.txt'],
    'bribri': ['bzd-x-bible-bzd-v1.txt'],
    'guarani': ['gug-x-bible-gug-v1.txt'],
    'hñähñu': ['ote-x-bible-ote-v1.txt'],
    'nahuatl': [
        # Yves: I would restrict the selection of Bibles to nch, ngu, nhe, nhw.
        'nch-x-bible-nch-v1.txt',
        'ngu-x-bible-ngu-v1.txt',
        'nhe-x-bible-nhe-v1.txt',
        'nhw-x-bible-nhw-v1.txt',
        # 'nah-NHXNTV.txt',
        # 'azz-x-bible-azz-v1.txt',
        # 'ncj-x-bible-ncj-v1.txt',
        # 'nhi-x-bible-nhi-v1.txt',
        # 'nhy-x-bible-nhy-v1.txt'
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


MONOLINGUAL = {
    'ashaninka': ['test.txt', 'train.txt', 'valid.txt'],
    'aymara': ['wiki.ay.aa'],
    'guarani': ['wiki.gn.aa'],
    'hñähñu': ['ote.txt'],
    'nahuatl': ['wikibooks.nah.aa', 'wiki.nah.aa'],
    'quechua': ['wikibooks.qu.aa', 'wiki.qu.aa'],
    'shipibo_konibo': ['test.txt', 'train.txt', 'valid.txt'],
    'wixarika': ['social.wix']
}


def get_bible_files(lang):
    return ['../data/bibles/{lang}/{fname}'.format(lang=lang, fname=fname) for fname in BIBLES[lang]]


def get_monolingual_files(lang):
    return ['../data/{lang}-spanish/mono/{fname}'.format(lang=lang, fname=fname)
            for fname in MONOLINGUAL[lang]]


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


# From https://github.com/pywirrarika/wixnlp/blob/master/normwix.py
def normwix(text):
    text = text.lower()
    text = re.sub(r"´", "'", text, flags=re.IGNORECASE)
    #text = re.sub(r"'", "", text, flags=re.IGNORECASE)
    text = re.sub(r"v", "w", text, flags=re.IGNORECASE)
    text = re.sub(r"(c|qu)", "k", text, flags=re.IGNORECASE)
    text = re.sub(r"[0-9]+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"ch", "ts", text, flags=re.IGNORECASE)
    text = re.sub(r"rr", "x", text, flags=re.IGNORECASE)
    text = re.sub(r" +", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[üï]", "+", text, flags=re.IGNORECASE)
    text = re.sub(r"^ ", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<!t|\[)s", "ts", text, flags=re.IGNORECASE)
    text = re.sub(r"[áàä]", "a", text, flags=re.IGNORECASE)
    text = re.sub(r"[éèë]", "e", text, flags=re.IGNORECASE)
    text = re.sub(r"[íì]", "i", text, flags=re.IGNORECASE)
    text = re.sub(r"[óòö]", "o", text, flags=re.IGNORECASE)
    text = re.sub(r"[úù]", "u", text, flags=re.IGNORECASE)


    text = re.sub(r"([a-z+])\1+", r"\1", text, flags=re.IGNORECASE)
    return text


class WixarikaNormalizer(opusfilter.PreprocessorABC):
    """Normalizer for the Wixarika bible corpus. Normalizes only the 2nd input file."""

    def process(self, pairs):
        for segments in pairs:
            output = []
            for idx, segment in enumerate(segments):
                output.append(normwix(segment) if idx == 1 else segment)
            yield output


# From data/bribri-spanish/bribri-orthography-conversion.ipynb
def convertToHumanSpelling(bribriInput, outputOrthography):
    bribriOutput = bribriInput
    punctuation = {
        " .": ".", " ,": ",", " !": "!", " ?": "?"
    }
    if (outputOrthography=="constenla"):

        # These use Sofía Flores' diacritic conventions,
        # where the line is a COMBINING MINUS SIGN BELOW 0x0320
        diacriticChars = {
            "ã":"a̠", "ẽ":"e̠","ĩ":"i̠", "õ":"o̠","ũ":"u̠",                  # Nasal low tone
            "áx":"á̠", "éx":"é̠", "íx":"í̠", "óx":"ó̠", "úx":"ú̠",           # Nasal falling tone
            "àx":"à̠", "èx":"è̠", "ìx":"ì̠", "òx":"ò̠", "ùx":"ù̠",           # Nasal high tone
            "âx":"â̠", "êx":"ê̠", "îx":"î̠", "ôx":"ô̠", "ûx":"û̠",           # Nasal rising tone
            "éq":"ë́", "óq":"ö́", "èq":"ë̀", "òq":"ö̀", "êq":"ë̂", "ôq":"ö̂"  # Lax vowels
        }
        for c in diacriticChars: bribriOutput = bribriOutput.replace(c, diacriticChars.get(c))
        for c in punctuation: bribriOutput = bribriOutput.replace(c, punctuation.get(c))
    elif (outputOrthography=="jara"):
        diacriticChars = {
            "ã":"ã","ẽ":"ẽ","ĩ":"ĩ","õ":"õ","ũ":"ũ",                # Nasal low tone
            "áx":"ã́","éx":"ẽ́","íx":"ĩ́","óx":"ṍ","úx":"ṹ",           # Nasal falling tone
            "àx":"ã̀","èx":"ẽ̀","ìx":"ĩ̀","òx":"õ̀","ùx":"ũ̀",           # Nasal high tone
            "âx":"ã̂","êx":"ẽ̂","îx":"ĩ̂","ôx":"õ̂","ûx":"ũ̂",           # Nasal rising tone
            "éq":"ë́","óq":"ö́","èq":"ë̀","òq":"ö̀","êq":"ë̂","ôq":"ö̂"   # Lax vowels
        }
        coromaChanges = {
            "tk":"tch",
            "Ñãlàx":"Ñõlòx","ñãlàx":"ñõlòx",                   # road
            "Káx":"Kóx","káx":"kóx",                           # place
            "Kàxlĩ":"Kòxlĩ","kàxlĩ":"kòxlĩ",                   # rain
            "Káxwötã'":"Kóxwötã'","káxwötã'":"kóxwötã'",       # need
            "Káxwötã":"Kóxwötã","káxwötã":"kóxwötã",           # need
            "Dakarò":"Krò","dakarò":"krò"                      # chicken
        }
        for c in coromaChanges: bribriOutput = bribriOutput.replace(c, coromaChanges.get(c))
        for c in diacriticChars: bribriOutput = bribriOutput.replace(c, diacriticChars.get(c))
        for c in punctuation: bribriOutput = bribriOutput.replace(c, punctuation.get(c))
    else:
        print("Please specify one of the two available systems: constenla, jara")
    return(bribriOutput)


class BribriNormalizer(opusfilter.PreprocessorABC):
    """Normalizer for the Bribri train/dev corpora. Normalizes only the 2nd input file."""

    def __init__(self, orthography='constenla', **kwargs):
        self.orthography = orthography
        super().__init__(**kwargs)

    def process(self, pairs):
        for segments in pairs:
            output = []
            for idx, segment in enumerate(segments):
                output.append(convertToHumanSpelling(
                    segment, self.orthography) if idx == 1 else segment)
            yield output


class RaramuriNormalizer(opusfilter.PreprocessorABC):
    """Normalizer for Raramuri data. Assumes Spanish - Raramuri input.

    Applies conversions mentioned in https://github.com/AmericasNLP/americasnlp2021/pull/5

    """

    tz2ch = (re.compile(r'tz'), 'ch')
    star_token = (re.compile(r' \* '), '')
    two_apostrophes_token = (re.compile(r" ` ' "), "’")
    apostrophe_token = (re.compile(r" ' "), "’")
    apostrophe_any = (re.compile(r"['`´]"), "’")

    def process(self, pairs):
        for segments in pairs:
            esp, tar = segments
            for pat, rep in [self.tz2ch, self.star_token, self.two_apostrophes_token,
                             self.apostrophe_token, self.apostrophe_any]:
                tar = re.sub(pat, rep, tar)
            yield esp, tar


class RaramuriTrainCleaner(opusfilter.PreprocessorABC):
    """Cleaner for Raramuri train data. Assumes Spanish - Raramuri input."""

    starting_cparen = re.compile(r'^[0-9a-z] \) ')
    starting_paren = re.compile(r'^(\( ([0-9]{1,2}|[a-z]) \) )+')
    ending_paren = re.compile(r' \( [0-9a-z] \)$')
    middle_paren = re.compile(r'\( [^\)]+? \)')

    def process(self, pairs):
        for segments in pairs:
            esp, tar = segments
            if re.match(self.starting_cparen, tar):
                # e ) ŕekó perá
                # 3 ) kepi tzo
                # a ) empolvarse
                tar = re.sub(self.starting_cparen, '', tar)
            if re.match(self.starting_cparen, esp):
                # a ) empolvarse
                # a ) hacerse neblina , formarse niebla
                esp = re.sub(self.starting_cparen, '', esp)
            if re.match(self.starting_paren, tar):
                # ( 1 ) ga'rá ka rá asiba !
                tar = re.sub(self.starting_paren, '', tar)
            if re.match(self.starting_paren, esp):
                # ( 1 ) hacer que se limpie
                esp = re.sub(self.starting_paren, '', esp)
            if re.search(self.ending_paren, tar):
                # bowérema ( 2 )
                tar = re.sub(self.ending_paren, '', tar)
            if not '(' in tar and re.search(self.middle_paren, esp):
                # otro que cayó ! ( en la trampa )
                # ( en ) El Yeso
                # ( se oye ) que ahí va una culebra !
                esp = re.sub(self.middle_paren, '', esp)
                esp = re.sub(r' +', ' ', esp)
            if ' , ' in esp and not ' , ' in tar and len(esp) > 1.5 * len(tar):
                # asiento , silla , banco
                # -> select first
                esp = esp.split(' , ')[0]
            yield esp, tar


class BlankFilter(opusfilter.FilterABC):
    """Filter out lines containing only BLANK (for data from Bibles)"""

    def score(self, pairs):
        for pair in pairs:
            yield [(sentence.strip() != 'BLANK') for sentence in pair]

    def accept(self, score):
        return all(score)


def main(config_output, workdir, single=None, tokenize=False, bibles=True, dev=True,
         monolingual=True, restricted_extra=False, filtering=True):
    # WORKDIR = 'processed_data'
    # OUTPUT = 'opusfilter.yaml'

    if single:
        logging.info("Creating config for %s data", single)
    if tokenize:
        logging.info("Tokenization enabled")
    if not bibles:
        logging.info("Bibles disabled")
    if not dev:
        logging.info("Dev sets disabled")
    if not monolingual:
        logging.info("Monolingual sets disabled")
    if restricted_extra:
        logging.info("Using restricted extra data")
        extra_datasets = RESTRICTED_EXTRA
    else:
        extra_datasets = EXTRA
    if not filtering:
        logging.info("Filtering disabled")

    steps = []

    # Preprocess/copy train sets
    for lang in LANGUAGES:
        if single and lang != single:
            continue
        inputs = get_input_files(lang, 'train')
        outputs = get_work_files(lang, 'train')
        preprocessors = []
        if lang == 'bribri':
            preprocessors.append({'BribriNormalizer': {}, 'module': 'create_opusfilter_config'})
        elif lang == 'raramuri':
            preprocessors.append({'RaramuriTrainCleaner': {}, 'module': 'create_opusfilter_config'})
            preprocessors.append({'RaramuriNormalizer': {}, 'module': 'create_opusfilter_config'})
        elif TOKENIZED_TRAIN[lang]:
            preprocessors.append({'Detokenizer': {
                'tokenizer': 'moses',
                'languages': ['es', LANGCODE[lang]]
            }})
        else:
            pass  # no preprocessing needed
        steps.append({
            'type': 'preprocess',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'preprocessors': preprocessors
            }
        })

    # Preprocess/copy dev sets
    if dev:
        for lang in LANGUAGES:
            if single and lang != single:
                continue
            inputs = get_input_files(lang, 'dev')
            outputs = get_work_files(lang, 'dev')
            preprocessors = []
            if lang == 'bribri':
                preprocessors.append({'BribriNormalizer': {}, 'module': 'create_opusfilter_config'})
            else:
                pass  # no preprocessing needed
            steps.append({
                'type': 'preprocess',
                'parameters': {
                    'inputs': inputs,
                    'outputs': outputs,
                    'preprocessors': preprocessors
                }
            })

    # Combine extra data sets
    for lang in extra_datasets:
        if single and lang != single:
            continue
        inputs = [get_input_files(lang, **params) for params in extra_datasets[lang]]
        for idx in [0, 1]:
            steps.append({
                'type': 'concatenate',
                'parameters': {
                    'inputs': [f[idx] for f in inputs],
                    'output': get_work_files(lang, 'extra-raw')[idx]
                }
            })

    # Preprocess/copy extra corpora
    for lang in extra_datasets:
        if single and lang != single:
            continue
        inputs = get_work_files(lang, 'extra-raw')
        outputs = get_work_files(lang, 'extra')
        preprocessors = []
        if lang == 'raramuri':
            preprocessors.append({'RaramuriNormalizer': {}, 'module': 'create_opusfilter_config'})
        else:
            pass  # no preprocessing needed
        steps.append({
            'type': 'preprocess',
            'parameters': {
                'inputs': inputs,
                'outputs': outputs,
                'preprocessors': preprocessors
            }
        })

    # Combine training and extra data sets
    for lang in LANGUAGES:
        if single and lang != single:
            continue
        inputs = [get_work_files(lang, 'train')]
        if lang in extra_datasets:
            inputs.append(get_work_files(lang, 'extra'))
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
        if single and lang != single:
            continue
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

    if filtering:
        # Remove duplicates
        for lang in LANGUAGES:
            if single and lang != single:
                continue
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
            if single and lang != single:
                continue
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
        output_prefix = 'dedup_filtered'
    else:
        output_prefix = 'input'

    # Bibles
    # * at most k=5 entries per line
    # * all tokenized -> detokenize
    # * wixarika should use normalization in normwix.py
    if bibles:
        for lang in LANGUAGES:
            if single and lang != single:
                continue
            inputs = [get_bible_files('spanish'), get_bible_files(lang)]
            raw = get_work_files(lang, 'bibles-raw')
            outputs = get_work_files(lang, 'bibles')
            filtered_outputs = get_work_files(lang, 'bibles_filtered')
            steps.append({
                'type': 'product',
                'parameters': {
                    'inputs': inputs,
                    'outputs': raw,
                    'skip_empty': True,
                    'skip_duplicates': True,
                    'k': 5,
                    'seed': 'bibles'
                }
            })
            preprocessors = []
            if lang == 'wixarika':
                preprocessors.append({'WixarikaNormalizer': {}, 'module': 'create_opusfilter_config'})
            elif lang == 'raramuri':
                preprocessors.append({'RaramuriNormalizer': {}, 'module': 'create_opusfilter_config'})
            preprocessors.append(
                {'Detokenizer': {
                    'tokenizer': 'moses',
                    'languages': ['es', LANGCODE[lang]]
                }}
            )
            steps.append({
                'type': 'preprocess',
                'parameters': {
                    'inputs': raw,
                    'outputs': outputs,
                    'preprocessors': preprocessors
                }
            })
            steps.append({
                'type': 'filter',
                'parameters': {
                    'inputs': outputs,
                    'outputs': filtered_outputs,
                    'filters': [
                        {'BlankFilter': {}, 'module': 'create_opusfilter_config'}
                    ]
                }
            })

    # Combine monolingual data sets
    if monolingual:
        for lang in MONOLINGUAL:
            if single and lang != single:
                continue
            inputs = get_monolingual_files(lang)
            output = get_work_files(lang, 'monolingual')[1]
            output_filtered = get_work_files(lang, 'monolingual_filtered')[1]
            steps.append({
                'type': 'concatenate',
                'parameters': {
                    'inputs': inputs,
                    'output': output
                }
            })
            steps.append({
                'type': 'filter',
                'parameters': {
                    'inputs': [output],
                    'outputs': [output_filtered],
                    'filters': [
                        {'LengthFilter': {'unit': 'word', 'min_length': 1, 'max_length': 500}}
                    ]
                }
            })

    if tokenize:
        # Tokenize training sets
        # FIXME: does not work properly at least for wixarika
        for lang in LANGUAGES:
            if single and lang != single:
                continue
            inputs = get_work_files(lang, output_prefix)
            outputs = get_work_files(lang, output_prefix + '_tokenized')
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
        for lang in LANGUAGES:
            if single and lang != single:
                continue
            inputs = get_work_files(lang, prefix='dev')
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

    logging.info("%s steps generated for %s", len(steps), config_output)

    # Write YAML configuration for opusfilter
    config = {
        'common': {
            'output_directory': workdir
        },
        'steps': steps
    }
    with open(config_output, 'w') as fobj:
        fobj.write(dump(config, Dumper=Dumper))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create OpusFilter configuration')
    parser.add_argument('output', metavar='FILE', help='OpusFilter config file')
    parser.add_argument('workdir', metavar='DIR', help='Work directory for OpusFilter')
    parser.add_argument('--no-bibles', dest='bibles', action='store_false', help='Exclude Bibles')
    parser.add_argument('--no-dev', dest='dev', action='store_false', help='Exclude dev sets')
    parser.add_argument('--no-monolingual', dest='monolingual', action='store_false', help='Exclude monolingual sets')
    parser.add_argument('--restricted-extra', dest='restricted_extra', action='store_true',
                        help='Exclude extra parallel data sets not provided by the organizers')
    parser.add_argument('--no-filtering', dest='filtering', action='store_false', help='Exclude filtering')
    parser.add_argument('--tokenize', action='store_true', help='Include tokenization')
    parser.add_argument('--single', default=None, help='Use single language')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(args.output, args.workdir, single=args.single, tokenize=args.tokenize,
         bibles=args.bibles, dev=args.dev, monolingual=args.monolingual,
         restricted_extra=args.restricted_extra, filtering=args.filtering)
