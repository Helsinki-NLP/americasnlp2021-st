#! /bin/bash -l

spm_train --input=es2_2M.txt --model_prefix=es2_16k --vocab_size=16000 --character_coverage=1.0 --model_type=unigram
spm_train --input=other2_2M.txt --model_prefix=other2_32k --vocab_size=32000 --character_coverage=1.0 --model_type=unigram

