


XMLFILES = ${wildcard */extra/*.xml}
XMLBASE  = ${basename ${basename ${XMLFILES}}}
XMLALG   = ${sort ${patsubst %,%.alignxml,${XMLBASE}}}
CORPUSFILES = ${patsubst %.xml,%.sentxml,${XMLFILES}}


.PHONY: align-xml
align-xml: ${XMLALG}


## add sentence IDs

${CORPUSFILES}: %.sentxml: %.xml
	perl -pe 'if (/<s/){$$i++;s/<s/<s id="$$i"/;}' < $< > $@


## sentence align and extract plain text

${XMLALG}:
	${MAKE} ${patsubst %.xml,%.sentxml,${wildcard ${@:.alignxml=}.*.xml}}
	echo ${firstword ${sort ${wildcard ${@:.alignxml=.*.sentxml}}}}
	echo ${lastword ${sort ${wildcard ${@:.alignxml=.*.sentxml}}}}
	uplug align/sent \
		-src ${firstword ${sort ${wildcard ${@:.alignxml=.*.sentxml}}}} \
		-trg ${lastword ${sort ${wildcard ${@:.alignxml=.*.sentxml}}}} \
	2> $@.log | iconv -f UTF-8 -t LATIN1 > $@
	opus2bitext \
	-e $(patsubst %.sentxml,%.sent,${firstword ${sort ${wildcard ${@:.alignxml=.*.sentxml}}}}) \
	-f $(patsubst %.sentxml,%.sent,${lastword ${sort ${wildcard ${@:.alignxml=.*.sentxml}}}}) \
	$@
