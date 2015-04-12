import ybc
import collections # provides Counter object
import sys
import kl

# Data structures provided by the ybc module:
# 
# class ybcCorpus:
#         .balungans = list()
# 
# class ybcBalungan:
#         .filename           complete path of source file
#         .shortname          short version of file name (automatically generated)
#         .gatras             list of ybcGatra instances (FLAT list of ybcGatra instances (all sections together)
#         .sections           list of ybcSection instances (includes embedded gatra list)
#         .scale              (automatically generated)
#         .mode               (automatically generated)
# 
# class ybcSection:
#         .gatras             list of ybcGatra instances
#         .name               name of section (from <S> tag in encoding)
#                  
# class ybcGatra:
#         .notes              list of ybcNote instances
#         
# class ybcNote:
#         .pitch              octave letter + scale degree number
#         .beat               0,1,2,3 plus decimals when beat is subdivided
#
#         .restDot            True/False depending on whether the notation has a rest dot
#                             (in this case .pitch has the value of the previously sounding pitch)     
#
#         .gong               True/False depending on whether gong is struck on this note
#         .nong               True/False depending on whether nong is struck on this note
#         .pul                True/False depending on whether pul is struck on this note

# substitute your local pathname here        
# download the corpus at https://github.com/eyequeue/yale-balungan-corpus/archive/master.zip
corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

modes = ['nem','sanga','manyura']			
unigrams = dict()
for m in modes:
	unigrams[m] = collections.Counter()

for b in corpus.balungans:
	for g in b.gatras:
		for n in g.notes:
			if not n.pul: continue
			for m in modes:
				if b.mode == m:
					unigrams[m][n.pitch] += 1
		
for m in modes:
	print m, unigrams[m]
	for p in sorted(unigrams[m]):
		print p, unigrams[m][p]
	
for m1 in modes:
	for m2  in modes:
		print "{} -> {}: {}".format(m1, m2, kl.KL(unigrams[m1],unigrams[m2]))
		
			
        
