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
#         .pitch = pitch      octave letter + scale degree number
#         .beat               0,1,2,3 plus decimals when beat is subdivided
#         
#         .gong               True/False depending on whether gong is struck on this note
#         .nong               True/False depending on whether nong is struck on this note
#         .pul                True/False depending on whether pul is struck on this note

# substitute your local pathname here        
# download the corpus at https://github.com/eyequeue/yale-balungan-corpus/archive/master.zip
corpus = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus')

for thisBalungan in corpus.balungans:

        output = '\n\n' + thisBalungan.filename + '\n\n'
        for thisGatra in thisBalungan.gatras:
            if len(thisGatra.notes) != 4:
                print output
                for thisNote in thisGatra.notes:
                    print thisNote
                output = ''
        
