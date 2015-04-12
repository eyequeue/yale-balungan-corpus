import ybc
import collections # provides Counter object
import sys
import kl


corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

# create data structures

modes = ['nem','sanga','manyura']			
unigrams = dict()
pitches = set()

for m in modes:
	unigrams[m] = collections.Counter()



for b in corpus.balungans:
	for g in b.gatras:
		for n in g.notes:
			if not (n.pul or n.nong or n.gong): continue
			for m in modes:
				if b.mode == m:
					unigrams[m][n.pitch] += 1   # add to unigram count for the relevant mode
				pitches.add(n.pitch) # add to set of all pitches

print "Unigram distributions:"
# print header
output = "{:10}".format('')  # add space where mode name will go in subsequent rows
for p in sorted(pitches):
	output += "{:^7}".format(p)  # 7 spaces for each pitch, centered
print output
		
# print unigram distribution for each mode
for m in modes:
	output = "{:10}".format(m)
	for p in sorted(pitches):
		output += "{:.3f}  ".format(1.0*unigrams[m][p]/sum(unigrams[m].values())) # 7 spaces for each pitch
	print output
	
# print KL distance for each pair of modes
print
print "KL divergences:"
for m1 in modes:
	for m2  in modes:
		print "{} -> {}: {}".format(m1, m2, kl.KL(unigrams[m1],unigrams[m2]))
		
			
        
