


XMLFILES = ${wildcard */extra/*.xml}
XMLBASE  = ${basename ${basename ${XMLFILES}}}
XMLALG   = ${sort ${patsubst %,%.alignxml,${XMLBASE}}}
CORPUSFILES = ${patsubst %.xml,%.sentxml,${XMLFILES}}


.PHONY: align-xml
align-xml: ${XMLALG}


## add sentence IDs

${CORPUSFILES}: %.sentxml: %.xml
	perl -pe 'if (/<s>/){$$i++;s/<s/<s id="$$i">/;}' < $< > $@


## sentence align and extract plain text

${XMLALG}:
	${MAKE} ${patsubst %.xml,%.sentxml,${wildcard ${@:.alignxml=}.*.xml}}
	echo ${firstword ${sort ${patsubst %.xml,%.sentxml,${wildcard ${@:.alignxml=}.*.xml}}}}
	echo ${lastword ${sort ${patsubst %.xml,%.sentxml,${wildcard ${@:.alignxml=}.*.xml}}}}
	uplug align/sent \
		-src ${firstword ${sort ${patsubst %.xml,%.sentxml,\
			${wildcard ${@:.alignxml=}.*.xml}}}} \
		-trg ${lastword ${sort ${patsubst %.xml,%.sentxml,\
			${wildcard ${@:.alignxml=}.*.xml}}}} 2> $@.log | \
	iconv -f UTF-8 -t LATIN1 > $@
	opus2bitext \
		-e ${dir $@}sent-${notdir $(patsubst %.sentxml,%,\
			${firstword ${sort ${patsubst %.xml,%.sentxml,\
				${wildcard ${@:.alignxml=}.*.xml}}}})} \
		-f ${dir $@}sent-${notdir $(patsubst %.sentxml,%,\
			${lastword ${sort ${patsubst %.xml,%.sentxml,\
				${wildcard ${@:.alignxml=}.*.xml}}}})} \
	$@
