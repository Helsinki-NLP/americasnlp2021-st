# ModelB fromSpanish

This is a multilingual model with Spanish as source language, used for the final submissions.

In the first phase of training, 90% of Spanish-English data is used. In the second phase of training (`finetune`), this proportion is reduced to about 50%.

`config.yaml` provides the OpenNMT-py configuration for phase 1. Step 72000 is selected as the basis for phase 2, due to best validation performance on the Spanish-English validation set.

`config_finetune_50dev.yaml` provides the OpenNMT-py configuration for the phase 2 model which includes 50% of the development set for training. Step 156000 is selected to produce the output of **submission 1** for all languages, on the basis of validation performance on an eleven-language validation set (containing WMT-News and the other 50% of the dev sets).

`config_finetune_100dev.yaml` provides the OpenNMT-py configuration for phase 3, using step 156000 of the above model as a basis. The 50% of the dev sets previously used for validation are now added to the training. Step 170000 is selected to produce the output of **submission 2** for all languages, on the basis of validation perplexity (although this does not mean much, since the validation data is now included in the training data).

`config_finetune_nodev.yaml` provides the OpenNMT-py configuration for the alternative phase 2 model that does not include development data for training. We chose one of three savepoints (74000, 118000, 150000) for each language according to the respective dev set performance (aym: 118000, bzd: 150000, cni: 150000, gn: 118000, hch: 150000, nah: 74000, oto: 118000, quy: 74000, shp: 118000, tar: 118000). This produces the output of **submission 5**.

`spm` contains the commands to produce the SentencePiece segmentation model. A common model for source and target side was used here.
