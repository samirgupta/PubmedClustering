import sys
from pprint import pprint
from time import time
import pickle

def processPubTatorFile(input_file_name):
    linesFH = open(input_file_name, "r")
    lines = linesFH.readlines()
    linesFH.close()
    t0 = time()
    pmid_disease_dict = dict()
    for line in lines:
        line = line.strip()
        tokens = line.split("\t")
        if len(tokens) == 4:
            pmid, mesh_id, dis_mens, dis_source = tokens[0:4]
            diseases = dis_mens.split("|")
            if pmid in pmid_disease_dict:
                pmid_disease_dict[pmid].extend(diseases)
            else:
                pmid_disease_dict[pmid] = diseases
    print("done in %fs" % (time() - t0))
    #print("abstracts downloaded: %d" % len(pmids))
    print()
    return pmid_disease_dict


def run():
    input_file_name = sys.argv[1]
    pmid_disease_dict = processPubTatorFile(input_file_name)
    file_name = './pubtator_dumps/pmid_disease_dict.pickle'
    with open(file_name, 'wb') as handle:
        pickle.dump(pmid_disease_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #pprint(pmid_disease_dict)

if __name__ == '__main__':
    run()
