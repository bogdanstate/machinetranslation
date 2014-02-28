import pickle
import sys, collections
counts = collections.defaultdict(collections.Counter)

for line in sys.stdin:
  [first, second, count] = line.strip().split('\t')
  count = int(count)
  counts[first][second] = count

bigrams_file = open('../../dictionaries/bigrams.pkl', 'wb')
pickle.dump(counts, bigrams_file)
bigrams_file.close()

