
SHELL = /bin/bash

processed_data: create_opusfilter_config.py
	python create_opusfilter_config.py opusfilter.yaml $@
	PYTHONPATH=. opusfilter opusfilter.yaml

processed_data_restricted_extra: create_opusfilter_config.py
	python create_opusfilter_config.py opusfilter_restricted_extra.yaml $@ --restricted-extra --no-bibles
	PYTHONPATH=. opusfilter opusfilter_restricted_extra.yaml

processed_data_no_filtering: create_opusfilter_config.py
	python create_opusfilter_config.py opusfilter_no_filtering.yaml $@ --no-filtering
	PYTHONPATH=. opusfilter opusfilter_no_filtering.yaml
