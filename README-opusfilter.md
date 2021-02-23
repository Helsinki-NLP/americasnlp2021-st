# Data filtering

Steps:

1) Install OpusFilter using `develop` branch (https://github.com/Helsinki-NLP/OpusFilter/tree/develop)

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
