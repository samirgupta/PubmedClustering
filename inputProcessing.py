
def process_pmids_file(input_file_pmids, is_labeled=False):
    """process input file and return pmids as list
       and labels if there
    
    Args:
        input_file_pmids (string): filename location
        is_labeled (bool, optional): is pmids labeled
    
    Returns:
        TYPE: tuple of [pmids] and [labels]
    """
    pmidsFH = open(input_file_pmids, "r")
    lines = pmidsFH.readlines()
    pmidsFH.close()
    pmids, labels = [], []
    for line in lines:
        line = line.strip()
        if is_labeled:
            tokens = line.split("\t")
            if len(tokens) == 2 and tokens[0].isdigit:
                pmids.append(tokens[0])
                labels.append(tokens[1])
        else:
            if line.isdigit:
                pmids.append(line)
    return (pmids,labels)
