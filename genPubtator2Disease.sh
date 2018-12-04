#!/bin/sh
rm -fv ./pubtator_dumps/disease2pubtator_filtered
rm -fv ./pmid_disease_dict.pickle
grep -f $1 ./pubtator_dumps/disease2pubtator | sort | uniq > ./pubtator_dumps/disease2pubtator_filtered
python dumpDiseaseDict.py ./pubtator_dumps/disease2pubtator_filtered
