import os
from os import listdir
import sys
import math

def get_file_paths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.i
    file_paths.sort()
    return file_paths 

def construct_ngram_model(unigram_count, bigram_count, file_paths):
    bigram_file = file_paths[0]
    unigram_file = file_paths[1]
    b_f = open(bigram_file, "r")
    for line in b_f:
        tokens = line.split('|')
        bigram = tokens[0]
        count = int(tokens[1])
        bigram_count[bigram] = count
    b_f.close()

def get_best_sent(fname, unigram_count, bigram_count):
    f = open(fname, "r")
    max_score = 0.0
    best_sent = f.readline()
    for line in f:
        score = 0.0
        tokens = line.split()
        for i in range(0, len(tokens)-1):
            token = tokens[i] + " " + tokens[i+1]
            if token in bigram_count:
                score += math.log10(bigram_count[token])
        if score > max_score:
            max_score = score
            best_sent = line
    f.close()
    return best_sent

if __name__ == "__main__":
    if len(sys.argv) != 4:
	print >> sys.stderr, 'usage: python scorer.py ngram_dir candidate_dir output_dir'
	os._exit(-1)

    ngram_dir = sys.argv[1]
    cand_dir = sys.argv[2]
    output_dir = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ngram_file_paths = get_file_paths(ngram_dir)
    
    unigram_count = {}
    bigram_count = {}
    construct_ngram_model(unigram_count, bigram_count, ngram_file_paths)

    cand_file_paths = get_file_paths(cand_dir)

    cum_trans_out = open(output_dir+"/translation_all.txt", "wb")
    for i in range(0, len(cand_file_paths)):
        #if os.path.exists(output_dir+"/translation"+str(i+1)+".txt"):
            #os.remove(output_dir+"/translation"+str(i+1)+".txt")
        indexes = [int(s) for s in cand_file_paths[i].split('_') if s.isdigit()]
        translation_out = open(output_dir+"/translation"+str(indexes[0])+".txt", "wb")
        best_sent = get_best_sent(cand_file_paths[i], unigram_count, bigram_count)
        translation_out.write(best_sent + "\n")
        cum_trans_out.write(str(indexes[0])+": "+best_sent + "\n")
        translation_out.close()
    cum_trans_out.close()
