from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans

def get_kmeans_cluster(doc_features, num_clusters, use_mini_batch=False, use_verbose=False):
    """Summary
    
    Args:
        doc_features (sparse matrix): tfidf sparse matrix
        num_clusters (integer): num of clusters
        use_mini_batch (bool, optional): use mini batch if true
        use_verbose (bool, optional): verbose
    
    Returns:
        numpy array: document labels
    """
    if use_mini_batch:
        km = MiniBatchKMeans(n_clusters=num_clusters, verbose=use_verbose)
    else:
        km = KMeans(n_clusters=num_clusters, verbose=use_verbose)
    km.fit(doc_features)
    doc_labels = km.labels_
    return doc_labels

def get_clustering_metrics(true_labels, pred_labels):
    """return clustering metrics
        Note these metrics are not affected by absolute 
        values of the labels
    
    Args:
        true_labels (array): true labels 
        pred_labels (array): labels produced by clustering
    
    Returns:
        TYPE: different clustering metrics
    """
    clustering_metrics = []
    clustering_metrics.append(("Homogeneity", metrics.homogeneity_score(true_labels, pred_labels)))
    clustering_metrics.append(("Completeness", metrics.completeness_score(true_labels, pred_labels)))
    clustering_metrics.append(("V-measure", metrics.v_measure_score(true_labels, pred_labels)))
    clustering_metrics.append(("Adjusted Rand-Index", metrics.adjusted_rand_score(true_labels, pred_labels)))
    return clustering_metrics

