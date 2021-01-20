# Data filtering

Steps:

1) Install OpusFilter using `nlingual-rebase` branch  (https://github.com/Helsinki-NLP/OpusFilter/tree/nlingual-rebase)

2) Create OpusFilter configuration using `processed_data` as work directory:

```
python create_opusfilter_config.py opusfilter.yaml processed_data
```

3) Run OpusFilter on the configuration:

```
opusfilter opusfilter.yaml
```

The filtered output files are in: `processed_data/[LANGUAGE]/dedup_filtered.[LANGCODE].gz`
