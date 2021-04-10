# ModelB toSpanish

This is a multilingual model with Spanish as target language, designed to create backtranslations. In the first phase of training, 90% of English-Spanish data is used. In the second phase of training (`finetune` folder), ten distinct models are created for each target language.

`config.yaml` provides the OpenNMT-py configuration for phase 1. Step 52000 is selected as the basis for phase 2, due to best validation performance on the English validation set.

`finetune/config_*.yaml` provides the OpenNMT-py configurations for the phase 2 models. Finetuning only improved validation performance for three languages (aym: 56000, hch: 64000, quy:60000). For the other languages, the 52000 savepoint of phase 1 is selected.

`translate_bt.sh` contains the commands for translating the monolingual data to Spanish, using the savepoints listed above.

`spm` contains the commands to produce the SentencePiece segmentation model. Note that distinct models are used for the source and the target languages.
