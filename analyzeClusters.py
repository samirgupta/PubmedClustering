import sys
import numpy as np
from pprint import pprint
from textProcessing import get_abstract_text
from textProcessing import get_pubtator_diseases
from textProcessing import get_doc_features
from textProcessing import get_doc_features_and_vectorizer
from inputProcessing import process_pmids_file
import pickle
file_name = './pubtator_dumps/pmid_disease_dict.pickle'
with open(file_name, 'rb') as handle:
    pmid_disease_dict = pickle.load(handle)
def getClusters(file_name):
    linesFH = open(file_name, "r")
    lines = linesFH.readlines()
    linesFH.close()
    cluster_dict = dict()
    for line in lines:
        line = line.strip()
        tokens = line.split()
        pmid, label = tokens[0:2]
        if label in cluster_dict: cluster_dict[label].append(pmid)
        else: cluster_dict[label] = [pmid]
    return cluster_dict

def getTrueLabels(file_name):
    linesFH = open(file_name, "r")
    lines = linesFH.readlines()
    linesFH.close()
    pmid_label_dict = dict()
    for line in lines:
        line = line.strip()
        tokens = line.split()
        pmid, label = tokens[0:2]
        pmid_label_dict[pmid] = label
    return pmid_label_dict

def getTopNFeatures(file_name):
    pmids, labels = process_pmids_file(file_name,True)
    abstract_texts = []
    top_features_dict = dict()
    for pmid in pmids:
        abstract_text = "None"
        abstract_text = get_abstract_text(pmid)
        #abstract_text = get_pubtator_diseases(pmid,pmid_disease_dict)
        abstract_texts.append(abstract_text)


    doc_features, tfidf = get_doc_features_and_vectorizer(abstract_texts)
    feature_array = np.array(tfidf.get_feature_names())
    for i,pmid in enumerate(pmids):
        tfidf_sorting = np.argsort(doc_features[i].toarray()).flatten()[::-1]
        n = 20 
        top_n = feature_array[tfidf_sorting][:n]
        top_features_dict[pmid] = top_n
    
    return top_features_dict

def printClusters(cluster_dict, pmid_label_dict, top_features_dict):
    for label in cluster_dict.keys():
        pmids = cluster_dict[label]
        print("Cluster #:"+ str(label)+"\n")
        for pmid in pmids:
            true_label = pmid_label_dict[pmid]
            abstract_text = get_abstract_text(pmid)
            #abstract_text = get_pubtator_diseases(pmid,pmid_disease_dict)
            print(pmid+ " :" + true_label)
            print("Top TF-IDF terms:")
            print(top_features_dict[pmid])
            print("\nTEXT: "+abstract_text)
            print("\n")
        print("\n=======================================\n")

def run():
    pmid_label_dict = getTrueLabels(sys.argv[1])
    top_features_dict = getTopNFeatures(sys.argv[1])
    cluster_dict = getClusters(sys.argv[2])
    printClusters(cluster_dict, pmid_label_dict, top_features_dict)

run()
