import ybc
import collections # provides Counter object
import sys
import kl


corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

# create data structures

modes = ['nem','manyura','sanga','all']
restsByBeat = dict()
for m in modes:
	restsByBeat[m] = collections.Counter()

for b in corpus.balungans:
	for g in b.gatras:
		for n in g.notes:
			if n.restDot:
				try:
					restsByBeat[b.mode][n.beat] += 1
				except:
					print b.filename
				restsByBeat['all'][n.beat] += 1

print "Distribution of rests over beat classes:"
# print header
output = "{:10}".format('')  # add space where mode name will go in subsequent rows
for p in sorted(restsByBeat['all']):
	output += "{:^7}".format(p)  # 7 spaces for each beat class, centered
print output
		
# print unigram distribution for each mode
for m in modes:
	output = "{:10}".format(m)
	for b in sorted(restsByBeat['all']):
		output += "{:.3f}  ".format(1.0*restsByBeat[m][b]/sum(restsByBeat[m].values())) # 7 spaces for each beat class
	print output
