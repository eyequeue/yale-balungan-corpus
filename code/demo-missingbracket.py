import ybc
import collections # provides Counter object
import sys
import kl


corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

# find corpus files with non-matching numbers of left and right brackets
# (brackets are encoded using section tags for now)

for b in corpus.balungans:
	rightBrackets = 0
	leftBrackets = 0
	for s in b.sections:
		if s.name == 'bracket start': leftBrackets += 1
		if s.name == 'bracket end': rightBrackets += 1
	if leftBrackets != rightBrackets:
		print "{} {} left brackets, {} right brackets".format(b.filename, leftBrackets, rightBrackets)
	