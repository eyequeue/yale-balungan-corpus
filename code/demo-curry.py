import ybc
import collections # provides Counter object
import sys
import kl


corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

# create data structures

modes = ['nem','sanga','manyura']			
unigrams = dict()
pitches = set()

data = dict()
for g in ['pul','nong','gong','total']: data[g] = dict()

for m in modes:
	data[m] = dict()
	for g in ['pul','nong','gong','total']: data[m][g] = collections.Counter()
	for b in corpus.balungans:
		if b.mode != m: continue
		for g in b.gatras:
			for n in g.notes:
				if n.pul: data[m]['pul'][n.pitch] += 1
				if n.nong: data[m]['nong'][n.pitch] += 1
				if n.gong: data[m]['gong'][n.pitch] += 1
				data[m]['total'][n.pitch] += 1
				if n.pitch != '': pitches.add(n.pitch)

print "Unigram distributions:"
print
for m in modes:
	# print header
	output = "{:10}".format(m)  # add space where mode name will go in subsequent rows
	for p in sorted(pitches):
		output += "{:>7}".format(p)  # 7 spaces for each pitch, centered
	print output
	
	for g in ['gong','nong','pul']:
		output = "{:10}".format(g)
		for p in sorted(pitches):
			output += "{:7}".format(data[m][g][p])  # 7 spaces for each pitch, centered
		print output
		
	print
	

sys.exit()

# print KL distance for each pair of modes
print
print "KL divergences:"
for m1 in modes:
	for m2  in modes:
		print "{} -> {}: {}".format(m1, m2, kl.KL(unigrams[m1],unigrams[m2]))
		
			
        
