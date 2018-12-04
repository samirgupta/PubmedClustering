import argparse

def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, 
                        help="input file containing pmids to cluster")
    parser.add_argument("output_file", type=str, 
                         help="output file to write cluster assignments")
    parser.add_argument("--num-clusters", dest="num_of_clusters", type=int, default=5,
                         help="number of clusters")
    parser.add_argument("--use-minibatch", dest="use_minibatch", default=False, action="store_true",
                         help="use mini batch k-means")
    parser.add_argument("--input-labeled", dest="input_labeled", default=False, action="store_true",
                         help="use labeled input file")
    parser.add_argument("--text-type", dest="text_type", type=str, default="abstract", choices=["abstract", "diseases"],
                         help="what terms to be considered in abstract for feature extraction: entire abstract (default) or only disease terms")
    args = parser.parse_args()
    return args
