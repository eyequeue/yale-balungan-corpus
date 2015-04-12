import ybc
import collections # provides Counter object
import sys

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

pitchUnigrams = collections.Counter()

for b in corpus.balungans:
	for g in b.gatras:
		for n in g.notes:
			pitchUnigrams[n.pitch] += 1
			
print pitchUnigrams
			
        
