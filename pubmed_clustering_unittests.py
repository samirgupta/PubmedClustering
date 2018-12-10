import sys
import unittest

from textProcessing import my_tokenizer
from textProcessing import get_abstract_text
from textProcessing import get_pubtator_diseases
from textProcessing import get_doc_features
from clustering import get_kmeans_cluster

class TestPubmedClustering(unittest.TestCase):

    """
    Test the text processing functions
    """


    def test_get_abstract_text(self):
        """
        Test the function that retrieves abstract text
        """
        #test_pmids = ["24619745",]
        result_text = get_abstract_text("24619745")
        expected_text = "Triple-negative breast carcinoma: current and emerging concepts. " \
                         "OBJECTIVES: Triple-negative breast cancer is regarded as an aggressive " \
                         "disease that affects a young patient population and for which effective " \
                         "targeted therapy is not yet available. METHODS: Intense efforts have " \
                         "been made to gain a better understanding of this heterogeneous group " \
                         "of tumors from the histologic to the genomic and molecular levels. " \
                         "RESULTS: Progress has been made, including the ability to subtype " \
                         "these tumors and the discovery of biomarkers toward which current " \
                         "therapeutic efforts are focused. Many novel targets under exploration " \
                         "have the potential to affect the clinical course of this disease. " \
                         "CONCLUSIONS: This article reviews the current concepts regarding the " \
                         "clinicopathologic features of triple-negative breast carcinoma, its " \
                         "histologic subtypes, molecular classification, the prognostic and " \
                         "therapeutic potential of biomarkers, and emerging targeted therapies."

        self.assertEqual(result_text, expected_text)

    def test_my_tokenizer(self):
        """
        Test the function that peforms tokenization and stemming
        """
        text_to_tokenize1 = "This is test sentence! This will test the tokenizer " \
                           "function, which first deletes punctuations, then tokenizes "\
                           "the text to list of tokens and then performs stemming."
        text_to_tokenize2 = "Do not perform stemming the text"

        result1 = my_tokenizer(text_to_tokenize1)
        result2 = my_tokenizer(text_to_tokenize2,stem=False)

        expected_result1 = ['test', 'sentenc', 'test', 'token', 'function', 'first', \
                            'delet', 'punctuat', 'token', 'text', 'list', 'token', \
                            'perform', 'stem']
        expected_result2 = ['perform', 'stemming', 'text']
        self.assertEqual(result1, expected_result1)
        self.assertEqual(result2, expected_result2)


    def test_get_doc_features(self):

        doc_texts = ["This is document1. This is about breast cancer.",
                     "This is document2. This is about prostate cancer."]

        doc_features1 = get_doc_features(doc_texts)
        doc_features2 = get_doc_features(doc_texts,max_ngram=2)

        ####sparse matrix of 2,11; 2 documents and 11 features
        ####since max_ngram by defaults is 3
        self.assertEqual(doc_features1.shape,(2,11))
        ####sparse matrix of 2,5; 2 documents and 9 features
        ####since max_ngram by provided is 2
        self.assertEqual(doc_features2.shape,(2,9))

    def test_get_kmeans_cluster(self):
        docs = ["This is document1 about breast cancer.",\
                "This is document2 about prostate cancer.",\
                "This is document3 about lung cancer.",\
                "This is document4 about breast cancer.",\
                "This is document5 about prostate cancer."]
        doc_features = get_doc_features(docs)
        
        ###test k-means with num_clusters = 3
        doc_labels = get_kmeans_cluster(doc_features,num_clusters=3)
        doc_labels_list = doc_labels.tolist()

        ####b-0,p-1,l-2; b-0,p-2,l-1; 
        ####b-1,p-0,l-2; b-1,p-2;l-0
        ####b-2;p-0,l-1; b-2,p-1,l-0
        expected_labels_all_permulations = [[0,1,2,0,1], [0,2,1,0,2],\
                                            [1,0,2,1,2], [1,2,0,1,2],\
                                            [2,0,1,2,0], [2,1,0,2,1]]
        self.assertEqual(len(doc_labels_list),5)
        self.assertIn(doc_labels_list,expected_labels_all_permulations)

         ###test k-means with num_clusters = 1
        doc_labels = get_kmeans_cluster(doc_features,num_clusters=1)
        doc_labels_list = doc_labels.tolist()

        self.assertEqual(len(doc_labels_list),5)
        self.assertEqual(doc_labels_list,[0,0,0,0,0])



if __name__ == '__main__':
    unittest.main()

