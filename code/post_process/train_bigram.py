import os
from os import listdir
import sys

def get_filepaths(directory):
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
            file_paths.append(filepath)  # Add it to the list.

    return file_paths 

def count_ngrams(fname, unigram_count, bigram_count):
    f = open(fname, "r")
    for line in f:
        tokens = line.split()
        for i in range(0, len(tokens)-1):
            token = tokens[i]
            # Count for the unigram count of this word
            if token in unigram_count:
                count = unigram_count[token] + 1
                unigram_count[token] = count
            else:
                unigram_count[token] = 1
            # Count for the bigram count of this_word + next_word
            token = token + " " + tokens[i+1]
            if token in bigram_count:
                count = bigram_count[token] + 1
                bigram_count[token] = count
            else:
                bigram_count[token] = 1
        # Count for the unigram count of the last word
        if len(tokens) > 0:
            last_token = tokens[len(tokens)-1]
            if last_token in unigram_count:
               count = unigram_count[last_token] + 1
               unigram_count[last_token] = count
            else:
               unigram_count[last_token] = 1
    f.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
	print >> sys.stderr, 'usage: python train_bigram.py data_dir output_dir'
	os._exit(-1)

    dev_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_paths = get_filepaths(dev_dir)
    unigram_count = {}
    bigram_count = {}
        
    for fname in file_paths:
        count_ngrams(fname, unigram_count, bigram_count)

    print >> sys.stdout, "Writing Unigram Count"
    unigram_out = open(output_dir+"/unigram", "wb")
    for token in unigram_count:
        if unigram_count[token] != 1:
            unigram_out.write(token + "|" + str(unigram_count[token]) + "\n")
    unigram_out.close()
    
    print >> sys.stdout, "Writing Bigram Count"
    bigram_out = open(output_dir+"/bigram", "wb")
    for token in bigram_count:
        if bigram_count[token] != 1:
            bigram_out.write(token + "|" + str(bigram_count[token]) + "\n")
    bigram_out.close()
