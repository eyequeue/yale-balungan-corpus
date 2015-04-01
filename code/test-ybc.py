import ybc
import collections # provides Counter object

# Data structures provided by the ybc module:
# 
# class ybcCorpus:
#         .balungans = list()
# 
# class ybcBalungan:
#         .filename           complete path of source file
#         .shortname          short version of file name (automatically generated)
#         .gatras             list of ybcGatra instances
#         .scale              (automatically generated)
#         .mode               (automatically generated)
# 
# class ybcGatra:
#         .notes              list of ybcNote instances
#         
# class ybcNote:
#         .pitch = pitch      octave letter + scale degree number
#         .beat               0,1,2,3 plus decimals when beat is subdivided
#         
#         .gong               True/False depending on whether gong is struck on this note
#         .nong               True/False depending on whether nong is struck on this note
#         .pul                True/False depending on whether pul is struck on this note

# substitute your local pathname here        
# download the corpus at https://github.com/eyequeue/yale-balungan-corpus/archive/master.zip
corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

gongTally = collections.Counter()
allTally = collections.Counter()

for thisBalungan in corpus.balungans:
    if thisBalungan.mode != 'manyura':
        continue
    for thisGatra in thisBalungan.gatras:
        for thisNote in thisGatra.notes:
            if thisNote.gong:
                gongTally[thisNote.pitch] += 1
            allTally[thisNote.pitch] += 1
            
                

print gongTally
print allTally