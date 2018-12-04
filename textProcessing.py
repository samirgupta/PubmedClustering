import sys
import requests
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint

def get_abstract_text(pmid):
    """Given a valid PMID download
        the abstract text from ncbi

    Args:
        pmid (string): PMID
    
    Returns:
        string: abstract text
    
    Raises:
        NameError: if invalid pmid
    """
    request_url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pubmed.cgi/BioC_json/'+pmid+'/unicode'
    res = requests.get(request_url)
    if res.status_code != 200:
        # This means something went wrong.
        raise NameError('GET PMID {} {}'.format(pmid,res.status_code))
    json_result = res.json()
    json_doc = None
    if 'documents' in json_result: json_doc = json_result['documents'][0]
    if json_doc:
        abstract_text, abstract_title = "",""
        passages = json_doc.get('passages',[])
        for passage in passages:
            if passage['infons']['type'] == "title": abstract_title = passage['text']
            elif passage['infons']['type'] == "abstract": abstract_text = passage['text']
        return abstract_title+" "+abstract_text
    return ""

def get_pubtator_entities(pmid):
    request_url = 'https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/BioConcept/'+pmid+'/JSON/'
    res = requests.get(request_url)
    print(request_url)
    print(res.text)
    if res.status_code != 200:
        # This means something went wrong.
        raise NameError('GET PMID {} {}'.format(pmid,res.status_code))
    json_result = res.json()
    #print(json_result)
    json_doc = None
    if len(json_result) == 1: json_doc = json_result[0]
    if json_doc:
        res_entities = []
        pubtator_entities = json_doc.get('denotations')
        for entity in pubtator_entities: res_entities.append(entity['obj'])
        return " ".join(res_entities)
    return ""

def my_tokenizer(text, stem=True):
    """Custom tokenizer converts text to list of tokens
    
    Args:
        text (string): document text to tokenize
        stem (bool, optional): perform steeming by default
    
    Returns:
        list: list of tokens
    """
    ##remove punctuation,stopwords and tokenize
    translator = str.maketrans('','',string.punctuation)
    text = text.translate(translator)
    tokens = nltk.word_tokenize(text.lower())
    stopwords_set = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stopwords_set] 

    ##perform stemming using Porter stemmer
    if stem:
        porter_stemmer = PorterStemmer()
        tokens = [porter_stemmer.stem(token) for token in filtered_tokens]

    return tokens

def get_doc_features(docs,max_features=None,max_ngram=3):
    """get document vectors using tf-idf
    
    Args:
        docs (list of string): list of documents 
        max_features (None, optional): max size of document vector (default: max)
        max_ngram (int, optional): max ngram to consider as feature
    
    Returns:
        sparse matrix, [n_samples, n_features]: tf-idf weighted document-term matrix
    """
    
    tfidf_vectorizer = TfidfVectorizer(max_features=max_features,
                                       tokenizer=my_tokenizer,
                                       ngram_range=(1,max_ngram))
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs)
    #print(tfidf_vectorizer.get_feature_names())
    return tfidf_matrix
