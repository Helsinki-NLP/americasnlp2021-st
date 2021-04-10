#! /bin/bash -l

spm_train --input=all2_3M.txt --model_prefix=all2_32k --vocab_size=32000 --character_coverage=1.0 --model_type=unigram

