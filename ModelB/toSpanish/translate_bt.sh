#! /bin/bash -l

module use -a /projappl/nlpl/software/modules/etc

SRCSPM=../../spm/other2_32k.model
TGTSPM=../../spm/es2_16k.model
DATADIR=../../americasnlp2021-st/processed_data/

declare -A LANG=( ["aym"]="aymara" ["cni"]="ashaninka" ["gn"]="guarani" ["hch"]="wixarika" ["nah"]="nahuatl" ["oto"]="hñähñu" ["quy"]="quechua" ["shp"]="shipibo_konibo" )
declare -A MODELS=( ["aym"]="../finetune/model_aym_step_56000.pt" ["cni"]="../model_step_52000.pt" ["gn"]="../model_step_52000.pt" ["hch"]="../finetune/model_hch_step_64000.pt" ["nah"]="../model_step_52000.pt" ["oto"]="../model_step_52000.pt" ["quy"]="../finetune/model_hch_step_60000.pt" ["shp"]="../model_step_52000.pt" )

module load nlpl-mttools

for LG in "${!LANG[@]}"; do
	spm_encode --model=$SRCSPM --output_format=piece < $DATADIR/"${LANG[$LG]}"/monolingual.$LG.txt | sed -e 's/^/__'"$LG"'__ /' > mono.$LG.tok
done

module load nlpl-opennmt-py

echo "Model file: $MODEL"

for LG in "${!MODELS[@]}"; do
	echo "$LG -- ${MODELS[$LG]}"
	onmt_translate -model "${MODELS[$LG]}" -src mono.$LG.tok -output mono_"$LG".es.tok -gpu 0
done

module load nlpl-mttools

for LG in "${!LANG[@]}"; do
	sed -e 's/^__[a-z]*__ //' mono_"$LG".es.tok | spm_decode --model=$TGTSPM --input_format=piece | sed -e 's/▁//g' > mono_"$LG".es.txt
done
