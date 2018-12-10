from argumentParsing import create_argument_parser
from inputProcessing import process_pmids_file
from textProcessing import my_tokenizer
from textProcessing import get_abstract_text
from textProcessing import get_pubtator_diseases
from textProcessing import get_doc_features
from clustering import get_kmeans_cluster
from clustering import get_clustering_metrics
from sklearn.decomposition import TruncatedSVD

from sklearn.manifold import TSNE
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

#%matplotlib inline

import pickle
import numpy as np
from time import time


def run():

    args = create_argument_parser()
    input_filename, is_labeled = args.input_file, args.input_labeled
    output_filename = args.output_file
    #input_filename, is_labeled = "./Data/pmids_gold.txt", False
    #input_filename, is_labeled = "./Data/pmids_gold_set_labeled.txt", True

    pmid_disease_dict = dict()
    text_type = args.text_type
    if text_type == "diseases":
        file_name = './pubtator_dumps/pmid_disease_dict.pickle'
        with open(file_name, 'rb') as handle:
            pmid_disease_dict = pickle.load(handle)


    pmids, labels = process_pmids_file(input_filename, is_labeled)

    
    true_labels = np.array(labels)
    #print(pmids)
    #print(true_labels)

    print("Extracting abstracts from NCBI and Preprocesing")
    t0 = time()
    abstract_texts = []
    for pmid in pmids:
        abstract_text = "None"
        if text_type == "abstract":
            abstract_text = get_abstract_text(pmid)
        elif text_type == "diseases":
            abstract_text = get_pubtator_diseases(pmid, pmid_disease_dict)
        #print((pmid,abstract_text))
        abstract_texts.append(abstract_text)
    print("done in %fs" % (time() - t0))
    print("abstracts downloaded: %d" % len(pmids))
    print()


    print("Extracting features from the dataset using tfidf")
    t0 = time()
    doc_features = get_doc_features(abstract_texts)
    print("done in %fs" % (time() - t0))
    print("n_samples: %d, n_features: %d" % doc_features.shape)
    print()

    X_reduced = TruncatedSVD(n_components=50, random_state=0).fit_transform(doc_features)
    X_embedded = TSNE(n_components=2).fit_transform(X_reduced)
    colors = {'TNBC (breast cancer)':'red',\
              'alzheimer’s disease':'green',\
              'Noonan':'blue',\
              'neurofibromatosis':'purple',\
              'Bardet-Biedl Syndrome Panel':'yellow'}
    colors_labels = [colors[x] for x in labels]
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(frameon=False)
    plt.setp(ax, xticks=(), yticks=())
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                    wspace=0.0, hspace=0.0)
    plt.scatter(X_embedded[:, 0], X_embedded[:, 1],
            c=colors_labels, marker="x")

    x_values = X_embedded[:, 0].tolist()
    y_values = X_embedded[:, 1].tolist()
    #print(type(X_embedded[:, 0]))
    #print(X_embedded[:, 0])
    for i, pmid in enumerate(pmids):
        ax.annotate(pmid, (x_values[i], y_values[i]))
    plt.show()
    print("Performing Clustering using k-means")
    t0 = time()
    num_clusters = args.num_of_clusters

    ###if using labeled data; use the number of labels as number of clusters
    if is_labeled:
        num_clusters = np.unique(true_labels).shape[0]
    doc_labels = get_kmeans_cluster(doc_features, num_clusters, use_mini_batch=args.use_minibatch)
    doc_labels_list = doc_labels.tolist()
    print("done in %fs" % (time() - t0))
    print("n_clusters: %d" % num_clusters)
    #print("Labels: ")
    #print(doc_labels_list)
    print()

    if is_labeled:
        print("Clustering Metrics")
        clustering_metrics = get_clustering_metrics(true_labels,doc_labels)
        for clustering_metric in clustering_metrics:
            print(clustering_metric[0]+":  %.3f" % clustering_metric[1])


    ###write cluster assignments to file
    with open(output_filename, 'w') as outputFH:
        for i,pmid in enumerate(pmids):
            cluster_label = doc_labels_list[i]
            outputFH.write(pmid+"\t"+str(cluster_label)+"\n")
        outputFH.close()



if __name__ == '__main__':
    run()
