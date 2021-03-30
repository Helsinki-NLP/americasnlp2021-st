# Data preparation

Steps:

1) Install OpusFilter version 2.0.0-beta (https://github.com/Helsinki-NLP/OpusFilter/tree/2.0.0-beta)

2) Create OpusFilter configuration using `processed_data` as work directory:

```
python create_opusfilter_config.py opusfilter.yaml processed_data
```

3) Run OpusFilter on the configuration:

```
PYTHONPATH=$PYTHONPATH:. opusfilter opusfilter.yaml
```
(PYTHONPATH added to include custom preprocessors in `create_opusfilter_config.py`.)

The filtered output files are in: `processed_data/[LANGUAGE]/dedup_filtered.[LANGCODE].gz`

See further examples in the Makefile.

The script `collect_data_sizes.py` can be used to collect a table of the number of lines in the produced files.
