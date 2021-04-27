# Translation results

## Simple bilingual baseline models

**(1) (Raul):**
- produced using the provided baseline system with the data without previous preprocessing

**(2) (Yves):**
- Standard transformers, 100k training steps
- SentencePiece joint 8k vocab
- evaluated on dev set

| Language pair | BLEU  | chrF2  | BLEU  | chrF2 | Language pair | BLEU  | chrF2 |
| ------------- | ----- | ------ | ----- | ----- | ------------- | ----- | ----- |
|               | (1)   | (1)    | (2)   | (2)   |               | (2)   | (2)   |
| es-aym        | 0.35  | 0.181 	| 0.937 | 0.232 | aym-es        | 2.666 | 0.211 |
| es-bzd        | 0.20  | 0.073 	| 0.820 | 0.113 |               |       |       |
| es-cni        |       |        | 0.100 | 0.195 | cni-es        | 0.711 | 0.159 |
| es-gn         |       |        | 3.430 | 0.238 | gn-es         | 4.613 | 0.237 |
| es-hch        | 4.26  | 0.119 	| 3.590 | 0.200 | hch-es        | 0.901 | 0.174 |
| es-nah        | 0.13  | 0.168 	| 0.164 | 0.207 | nah-es        | 1.274 | 0.170 |
| es-oto        |       |        | 0.027 | 0.108 | oto-es        | 0.281 | 0.147 |
| es-quy        |       |        | 1.205 | 0.275 | quy-es        | 4.870 | 0.250 |
| es-shp        |       |        | 0.544 | 0.187 | shp-es        | 1.448 | 0.165 |
| es-tar        | 0.01  | 0.046 	| 0.056 | 0.143 |               |       |       |


## Multilingual models for X -> Spanish (back-translation)

**Model A (Raul):**
- multilingual model without English
- no backtranslations added
- standard transformer with language tags in the src sentence
- many-to-many 200k steps

**Model A+BT (Raul):**
- same as A, but with added backtranslations

**Model B' (Yves):**
- High-capacity transformers
- Pretraining: 90% English, 10% remaining languages
- SentencePiece separate vocabs: 16k es, 32k en+other
- Evaluated on dev set after 52k pretraining steps (no finetuning)

| Language pair | BLEU | chrF2 | BLEU | chrF2 | BLEU  | chrF2 |
| ------------- | ---- | ----- | ---- | ----- | ----- | ----- |
|               | A    | A     | A+BT | A+BT  | B'    | B'    |
| aym-es        | 4.40 | 0.221 | 4.67 | 0.220 | 8.833	| 0.270	|
| bzd-es        | 5.23 | 0.249 | 5.39 | 0.255 | 9.744	| 0.316	|
| cni-es        | 3.39 | 0.199 | 3.56 | 0.193 | 4.558	| 0.211	|
| gn-es         | 4.98 | 0.238 | 5.54 | 0.244 | 9.696	| 0.296	|
| hch-es        | 4.35 | 0.232 | 4.23 | 0.230 | 7.025	| 0.268	|
| nah-es        | 3.80 | 0.218 | 4.27 | 0.220 | 8.629	| 0.275	|
| oto-es        | 1.60 | 0.175 | 1.35 | 0.176 | 1.837	| 0.172	|
| quy-es        | 5.77 | 0.271 | 6.37 | 0.273 | 9.555	| 0.302	|
| shp-es        | 5.85 | 0.256 | 6.82 | 0.265 | 10.31	| 0.323	|
| tar-es        | 1.19 | 0.189 | 1.21 | 0.188 | 3.141	| 0.213	|


## Multilingual models for Spanish -> X (without dev set, track 2)

**Model A (Raul):**
- multilingual model without English
- no backtranslations added
- standard transformer with language tags in the src sentence
- many-to-many 200k steps

**Model A+BT (Raul):**
- same as A, but with added backtranslations

**Model B (Yves):**
- High-capacity transformers (run 3 with data bug fixes and joint vocab)
- Pretraining: 90% English, 10% remaining languages
- SentencePiece joint 32k vocab
- Evaluated on dev set after 72k pretraining steps (no finetuning, no backtranslations)

**Model B+FT74 (Yves):**
- Finetuning from step 72k to step 74k
- 50% English, 50% remaining languages
- Backtranslations included

**Model B+FT118 (Yves):**
- Same as above, but finetuning from step 72k to step 118k

**Model B+FT156 (Yves):**
- Same as above, but finetuning from step 72k to step 156k

**Model C (Jörg):**
- with OPUS data, no backtranslations

**Model C+BT (Jörg):**
- with OPUS data, with backtranslations

| Language pair | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 |
| ------------- | ---- | ----- | ---- | ----- | ---- | ----- | ---- | ----- | ---- | ----- | ---- | ----- | ---- | ----- | ---- | ----- |
|  | A | | A+BT |  | B |  | B+FT74 |  | B+FT118 |  | B+FT150 |  | C |  | C+BT |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| es-aym | 3.4 | 0.223 | 3.22 | 0.245 | 3.374 | 0.306 | 4.442 | 0.322 | **4.524** | **0.327** | 4.207 | 0.324 | 2.9 | 0.291 | 3.6 | 0.295 |
| es-bzd | 3.35 | 0.203 | 3.39 | 0.188 | 4.773 | 0.225 | 5.169 | 0.232 | 5.115 | 0.233 | **5.274** | **0.238** | 3.1 | 0.183 | 3.4 | 0.183 |
| es-cni | 2.36 | 0.222 | 2.78 | 0.24 | 2.636 | 0.239 | **2.967** | 0.255 | 2.473 | 0.255 | 2.73 | 0.268 | 1.4 | 0.25 | 1.8 | **0.271** |
| es-gn | 3.88 | 0.247 | 4.05 | 0.26 | 5.345 | 0.299 | 5.096 | 0.299 | **5.449** | **0.311** | 5.424 | **0.311** | 2.8 | 0.258 | 3.7 | 0.278 |
| es-hch | 6.32 | 0.258 | 7.22 | 0.255 | **8.669** | **0.303** | 6.582 | 0.29 | 6.398 | 0.289 | 7.325 | 0.299 | 7.3 | 0.267 | 7 | 0.267 |
| es-nah | 2.05 | 0.242 | 2.67 | 0.251 | 2.681 | 0.279 | **3.471** | **0.298** | 3.051 | 0.284 | 2.927 | 0.273 | 1.6 | 0.26 | 2.6 | 0.237 |
| es-oto | 1.08 | 0.137 | 0.97 | 0.138 | 1.043 | 0.139 | 1.104 | 0.142 | **1.143** | **0.147** | 1.022 | 0.146 | 0.3 | 0.12 | 0.5 | 0.129 |
| es-quy | 2.34 | 0.206 | 2.92 | 0.245 | 2.22 | 0.265 | **3.889** | **0.338** | 3.479 | 0.326 | 3.462 | 0.316 | 2.1 | 0.285 | 2.8 | 0.303 |
| es-shp | 2.1 | 0.158 | 4.58 | 0.292 | 4.519 | 0.299 | 4.69 | 0.259 | **5.627** | **0.317** | 5.402 | **0.317** | 1.6 | 0.182 | 3.3 | 0.241 |
| es-tar | **1.21** | 0.162 | 1.04 | 0.159 | 1.184 | 0.173 | 1.092 | 0.185 | 1.551 | **0.196** | 1.138 | 0.19 | 0.4 | 0.175 | 0.9 | 0.181 |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Mean | 2.809 | 0.2058 | 3.284 | 0.2273 | 3.6444 | 0.2527 | 3.8502 | 0.262 | 3.881 | **0.2685** | **3.8911** | 0.2682 | 2.35 | 0.2271 | 2.96 | 0.2385 |


## Multilingual models for Spanish -> X (with dev set, track 1)

**Model A25 (Raul):**
- multilingual model without English
- finetuning from step 200k to 202.5k with 50% of dev set

**Model A50 (Raul):**
- multilingual model without English
- finetuning from step 200k to 205k with 50% of dev set

**Model B (Yves):**
- Finetuning from step 72k to step 156k
- 50% English, 50% remaining languages
- Backtranslations + 50% of dev set included

All evaluations on the other 50% of the dev set.

| Language pair | BLEU | chrF2 | BLEU | chrF2 | BLEU | chrF2 |
| ------------- | ---- | ----- | ---- | ----- | ---- | ----- |
|  | A25 | | A50 |  | B |  |
|  |  |  |  |  |  |  |
| es-aym | 6.36 | 0.323 | 6.43 | 0.330 | 9.326 | 0.39 |
| es-bzd | 11.70 | 0.322 | 11.47 | 0.316 | 16.977 | 0.392 |
| es-cni | 9.80 | 0.382 | 9.27 | 0.385 | 8.332 | 0.414 |
| es-gn | 8.03 | 0.337 | 8.06 | 0.337 | 11.072 | 0.408 |
| es-hch | 14.83 | 0.351 | 13.99 | 0.340 | 19.637 | 0.409 |
| es-nah | 7.43 | 0.358 | 5.93 | 0.359 | 8.779 | 0.426 |
| es-oto | 7.10 | 0.251 | 6.50 | 0.247 | 12.14 | 0.313 |
| es-quy | 5.23 | 0.361 | 4.94 | 0.360 | 8.456 | 0.457 |
| es-shp |      |       |      |       | 12.238 | 0.452 |
| es-tar | 5.23 | 0.264 | 5.61 | 0.272 | 6.856 | 0.317 |

## Multilingual models without English (Raul)
 - standard transformer with language tags in the src sentence
 - many-to-many 200k steps
 

| Language pair | BLEU  | chrF2 | Language pair | BLEU  | chrF2 |
| ------------- | ----- | ----- | ------------- | ----- | ----- |
| es-aym        | 3.40 | 0.223 | aym-es        | 4.40 | 0.221 |
| es-bzd        | 3.35 | 0.203 | bzd-es        | 5.23 | 0.249 |
| es-cni        | 2.36 | 0.222 | cni-es        | 3.39 | 0.199 |
| es-gn         | 3.88 | 0.247 | gn-es         | 4.98 | 0.238 |
| es-hch        | 6.32 | 0.258 | hch-es        | 4.35 | 0.232 |
| es-nah        | 2.05 | 0.242 | nah-es        | 3.80 | 0.218 |
| es-oto        | 1.08 | 0.137 | oto-es        | 1.60 | 0.175 |
| es-quy        | 2.34 | 0.206 | quy-es        | 5.77 | 0.271 |
| es-shp        | 2.10 | 0.158 | shp-es        | 5.85 | 0.256 |
| es-tar        | 1.21 | 0.162 | tar-es        | 1.19 | 0.189 |

## Multilingual models with backtranslation without English (Raul)
 - standard transformer with language tags in the src sentence
 - many-to-many 200k steps
 

| Language pair | BLEU  | chrF2 | Language pair | BLEU  | chrF2 |
| ------------- | ----- | ----- | ------------- | ----- | ----- |
| es-aym        | 3.22 | 0.245 | aym-es        | 4.67 | 0.220 |
| es-bzd        | 3.39 | 0.188 | bzd-es        | 5.39 | 0.255 |
| es-cni        | 2.78 | 0.240 | cni-es        | 3.56 | 0.193 |
| es-gn         | 4.05 | 0.260 | gn-es         | 5.54 | 0.244 |
| es-hch        | 7.22 | 0.255 | hch-es        | 4.23 | 0.230 |
| es-nah        | 2.67 | 0.251 | nah-es        | 4.27 | 0.220 |
| es-oto        | 0.97 | 0.138 | oto-es        | 1.35 | 0.176 |
| es-quy        | 2.92 | 0.245 | quy-es        | 6.37 | 0.273 |
| es-shp        | 4.58 | 0.292 | shp-es        | 6.82 | 0.265 |
| es-tar        | 1.04 | 0.159 | tar-es        | 1.21 | 0.188 |

## Multilingual models with English (Yves)

- High-capacity transformers
- Pretraining: 90% English, 10% remaining languages
- SentencePiece separate vocabs: 16k es, 32k en+other
- Evaluated on dev set after 40k pretraining steps

| Language pair | BLEU  | chrF2 | Language pair | BLEU  | chrF2 |
| ------------- | ----- | ----- | ------------- | ----- | ----- |
| es-en        | 31.138 | 0.556 | en-es        | 32.214 | 0.572 |
| es-aym        | 3.867 | 0.307 | aym-es        | 8.628 | 0.271 |
| es-bzd        | 5.765 | 0.233 | bzd-es        | 8.673 | 0.310 |
| es-cni        | 2.525 | 0.239 | cni-es        | 3.916 | 0.215 |
| es-gn         | 5.877 | 0.296 | gn-es        | 10.135 | 0.294 |
| es-hch        | 7.462 | 0.286 | hch-es        | 5.998 | 0.260 |
| es-nah        | 3.118 | 0.267 | nah-es        | 8.636 | 0.273 |
| es-oto        | 1.022 | 0.142 | oto-es        | 1.536 | 0.166 |
| es-quy        | 3.314 | 0.325 | quy-es        | 8.742 | 0.287 |
| es-shp        | 4.455 | 0.299 | shp-es       | 11.362 | 0.340 |
| es-tar        | 1.090 | 0.172 | tar-es        | 1.663 | 0.196 |

- High-capacity transformers (run 3 with data bug fixes and joint vocab)
- Pretraining: 90% English, 10% remaining languages
- SentencePiece joint 32k vocab
- Evaluated on dev set after 72k pretraining steps

| Language pair | *LC BLEU* | *BLEU* | *chrF2* | | *BLEU* | *chrF2* |
| ------------- | ----- | ----- | ----- | --- |  ----- | ----- |
|               | *Full devset*  | | | | *Half devset* | |
| es-en         | 32.635 | 31.703 | 0.567 | |      |       |
| es-aym        | 3.500 | 3.374 | 0.306 | |  3.544 | 0.302 |
| es-bzd        | 5.446 | 4.773 | 0.225 | |  5.292 | 0.229 |
| es-cni        | 2.766 | 2.636 | 0.239 | |  1.925 | 0.236 |
| es-gn         | 5.702 | 5.345 | 0.299 | |  5.170 | 0.300 |
| es-hch        | 8.803 | 8.669 | 0.303 | |  8.864 | 0.302 |
| es-nah        | 2.959 | 2.681 | 0.279 | |  2.494 | 0.274 |
| es-oto        | 1.085 | 1.043 | 0.139 | |  0.989 | 0.138 |
| es-quy        | 2.413 | 2.220 | 0.265 | |  2.709 | 0.272 |
| es-shp        | 4.681 | 4.519 | 0.299 | |  4.449 | 0.297 |
| es-tar        | 1.297 | 1.184 | 0.173 | |  1.153 | 0.175 |

- Finetuning: 50% English, 50% one American language pair
- Evaluated on dev set after 72k pretraining steps + 4k fine-tuning steps

| Language pair | *BLEU* | *chrF2* | | *BLEU* | *chrF2* |
| ------------- | ----- | ----- | --- |  ----- | ----- |
|               | *Full devset*  | | | *Half devset* | |
| es-en         |       |       | |       |       |
| es-aym        | 4.061 | 0.325 | | 4.432 | 0.326 |
| es-bzd        | 4.498 | 0.226 | | 4.704 | 0.227 |
| es-cni        | 2.325 | 0.272 | | 2.026 | 0.267 |
| es-gn         | 5.397 | 0.320 | | 5.546 | 0.322 |
| es-hch        | 7.310 | 0.297 | | 7.493 | 0.300 |
| es-nah        | 3.250 | 0.289 | | 3.847 | 0.292 |
| es-oto        | 0.917 | 0.140 | | 0.900 | 0.138 |
| es-quy        | 3.062 | 0.281 | | 3.549 | 0.285 |
| es-shp        | 4.391 | 0.300 | | 4.257 | 0.299 |
| es-tar        | 1.017 | 0.190 | | 1.106 | 0.189 |

## Multilingual models with OPUS data, without backtranslations (Jörg)

| Language pair | *BLEU* | *chrF2* |
| ------------- | ----- | ----- |
| es-aym        | 2.9 | 0.291 |
| es-bzd        | 3.1 | 0.183 |
| es-cni        | 1.4 | 0.250 |
| es-gn         | 2.8 | 0.258 |
| es-hch        | 7.3 | 0.267 |
| es-nah        | 1.6 | 0.260 |
| es-oto        | 0.3 | 0.120 |
| es-quy        | 2.1 | 0.285 |
| es-shp        | 1.6 | 0.182 |
| es-tar        | 0.4 | 0.175 |


## Multilingual models with OPUS data, with backtranslations (Jörg)

| Language pair | *BLEU* | *chrF2* |
| ------------- | ----- | ----- |
| es-aym        | 3.6 | 0.295 |
| es-bzd        | 3.4 | 0.183 |
| es-cni        | 1.8 | 0.271 |
| es-gn         | 3.7 | 0.278 |
| es-hch        | 7.0 | 0.267 |
| es-nah        | 2.6 | 0.237 |
| es-oto        | 0.5 | 0.129 |
| es-quy        | 2.8 | 0.303 |
| es-shp        | 3.3 | 0.241 |
| es-tar        | 0.9 | 0.181 |
