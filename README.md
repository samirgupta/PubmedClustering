# PubmedClustering
Cluster pubmed abstracts using k-means

Tested on Python version: 3.6.3

see ./requirements.txt for other dependencies


usage: test.py [-h] [--num-clusters NUM_OF_CLUSTERS] [--use-minibatch]

               [--input-labeled] [--text-type {abstract,diseases}]
               
               input_file output_file

positional arguments:

  input_file            input file containing pmids to cluster
  
  output_file           output file to write cluster assignments
  

optional arguments:

  -h, --help            show this help message and exit
  
  --num-clusters NUM_OF_CLUSTERS
  
                        number of clusters
                        
  --use-minibatch       use mini batch k-means
  
  --input-labeled       use labeled input file
  
  --text-type {abstract,diseases}
  
                        what terms to be considered in abstract for feature
                        
                        extraction: entire abstract (default) or only disease
                        
                        terms
                        
Sample Usage: 

####use --input_labeled option to specify is input file is labeled
####if labeled file used some clustering metrics are also displayed in stdout
####if labeled the number of unique labels is used as number of clusters
python test.py Data/pmids_gold_set_labeled.txt Output/cluster_output --input_labeled

###sample usage if inputfile is unlabeled
python test.py Data/pmids_gold_set_unlabeled.txt Output/cluster_output

###can specify number of clusters
python test.py Data/pmids_gold_set_unlabeled.txt Output/cluster_output --num-cluster=4


Note there is an option --text-type ("abstract" by default) to use entire text as feature extraction or only disease terms for a pmid
Sample Usage

##use only disease mentions from pubtator as token text of a pmid for feature extraction
python test.py Data/pmids_gold_set_labeled.txt Output/cluster_output --input_labeled --text-type=diseases

Note: (only for --text-type=diseases option)

The restful APIs provided by NCBI to access pubtator annotations (https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/usage/)
is not stable. After multiple requests it sends 502 bad gateway error. To resolve this I have used downloadable databases (might miss some latest PMIDs) of pubtator annotations from (ftp://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator/). Use ./genPubtator2Disease.sh <pmidsFile> to generate pubtator disease annotations for new pmids. Since the actual filesize of disease2pubtator is very large and not accepted by github, a local copy of pubtator disease annotation for all gold set and test set pmids is provided and can be found at ./pubtator_dumps/disease2pubtator. Uncomment lines 2-5 in ./genPubator2Disease.sh to download the full file.






