





# Pubmed Clustering Problem

These PMIDs are the partial results of PubMed searches for different diseases which were subsequently combined and shuffled. We would like you to retrieve the abstracts for those PMIDs and cluster them into groups that would ideally match the search query results.

Three files have been provided for you: 

1. pmids_gold_set_labeled.txt contains a 'gold set' of PMIDs labeled with the search terms used to retrieve them
2. pmids_gold_set.txt contains the gold set, combined and shuffled
3. pmids_unlabeled.txt contains PMIDs with no search term labels

Please create a git repository that contains your code for retrieving the abstracts and generating the clusters.  The repo should contain a README that provides instructions on how to build and run your code. Please assume we'll be running the code on a default Ubuntu 16.04 instance. List any required dependencies.  The code will take as input the list of PMIDs and output the clusters.

Describe:

1. The text processing steps used (tokenization, stemming, etc).
2. The similarity metric employed for the clustering algorithm.
3. The clustering algorithm chosen.
4. The parameters tested/used to execute the clustering algorithm.
5. Design choices and computational complexity of your code
6. If you had the correct groupings of the PMIDs, how would your evaluate the performance of your clustering algorithm?
