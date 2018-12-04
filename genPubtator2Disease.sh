#!/bin/sh
#wget ftp://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator/disease2pubtator.gz
#gzip -d disease2pubtator_filtered
#rm -rfv ./pubtator_dumps/disease2pubtator
#mv ./disease2pubtator ./pubtator_dumps/disease2pubtator

rm -fv ./pubtator_dumps/disease2pubtator_filtered
rm -fv ./pmid_disease_dict.pickle
grep -f $1 ./pubtator_dumps/disease2pubtator | sort | uniq > ./pubtator_dumps/disease2pubtator_filtered
python dumpDiseaseDict.py ./pubtator_dumps/disease2pubtator_filtered
