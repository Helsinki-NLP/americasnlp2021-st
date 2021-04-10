#! /bin/bash

declare -A LANG=( ["cni"]="ashaninka" ["aym"]="aymara" ["bzd"]="bribri" ["gn"]="guarani" ["oto"]="hñähñu" ["nah"]="nahuatl" ["quy"]="quechua" ["tar"]="raramuri" ["shp"]="shipibo_konibo" ["hch"]="wixarika")

PDIR="../americasnlp2021-st/processed_data"
ENDIR="../spa-eng/opusdata"

echo "" > es_all.txt
for LG in "${!LANG[@]}"; do
	echo "$LG - ${LANG[$LG]}"
	zcat $PDIR/"${LANG[$LG]}"/bibles.$LG.gz $PDIR/"${LANG[$LG]}"/dedup_filtered.$LG.gz $PDIR/"${LANG[$LG]}"/monolingual.$LG.gz | sort -u | shuf > "$LG"_dedup.txt
	cat "$LG"_dedup.txt "$LG"_dedup.txt "$LG"_dedup.txt "$LG"_dedup.txt "$LG"_dedup.txt "$LG"_dedup.txt "$LG"_dedup.txt | head -n 100000 | shuf > "$LG"_100k.txt
	zcat $PDIR/"${LANG[$LG]}"/bibles.es.gz $PDIR/"${LANG[$LG]}"/dedup_filtered.es.gz >> es_all.txt
done

zcat $ENDIR/other_filt.es.gz es_all.txt | sort -u | shuf | head -n 2000000 > es2_2M.txt
zcat $ENDIR/other_filt.en.gz | sort -u | shuf | head -n 1000000 > en2_1M.txt
cat *_100k.txt en2_1M.txt | shuf > other2_2M.txt

wc *.txt
