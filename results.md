# Translation results

## Simple bilingual models

- Standard transformers, 100k training steps
- SentencePiece joint 8k vocab
- evaluated on dev set

| Language pair | BLEU  | chrF2 | Language pair | BLEU  | chrF2 |
| ------------- | ----- | ----- | ------------- | ----- | ----- |
| es-aym        | 0.937 | 0.232 | aym-es        | 2.666 | 0.211 |
| es-bzd        | 0.820 | 0.113 |               |       |       |
| es-cni        | 0.100 | 0.195 | cni-es        | 0.711 | 0.159 |
| es-gn         | 3.430 | 0.238 | gn-es         | 4.613 | 0.237 |
| es-hch        | 3.590 | 0.200 | hch-es        | 0.901 | 0.174 |
| es-nah        | 0.164 | 0.207 | nah-es        | 1.274 | 0.170 |
| es-oto        | 0.027 | 0.108 | oto-es        | 0.281 | 0.147 |
| es-quy        | 1.205 | 0.275 | quy-es        | 4.870 | 0.250 |
| es-shp        | 0.544 | 0.187 | shp-es        | 1.448 | 0.165 |
| es-tar        | 0.056 | 0.143 |               |       |       |


## Multilingual models without English (Raul)

| Language pair | BLEU  | chrF2 | Language pair | BLEU  | chrF2 |
| ------------- | ----- | ----- | ------------- | ----- | ----- |
| es-aym        | 5.44 | 0.290 | aym-es        | 7.38 | 0.278 |
| es-bzd       | 11.40 | 0.315 | bzd-es        | 8.44 | 0.310 |
| es-cni        | 3.80 | 0.287 | cni-es        | 6.10 | 0.247 |
| es-gn         | 8.50 | 0.298 | gn-es         | 7.97 | 0.315 |
| es-hch        | 7.16 | 0.307 | hch-es        | 7.63 | 0.297 |
| es-nah        | 4.11 | 0.292 | nah-es        | 5.61 | 0.301 |
| es-oto        | 2.16 | 0.178 | oto-es        | 3.78 | 0.204 |
| es-quy        | 5.48 | 0.306 | quy-es        | 9.63 | 0.364 |
| es-shp        | 5.05 | 0.246 | shp-es        | 9.93 | 0.333 |
| es-tar        | 3.32 | 0.212 | tar-es        | 2.46 | 0.200 |


## Multilingual models with English

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
