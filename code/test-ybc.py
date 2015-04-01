import ybc
import collections # provides Counter object

gongTally = collections.Counter()
allTally = collections.Counter()

for thisBalungan in ybc.ybcCorpus:
    for thisGatra in thisBalungan.gatras:
        for thisNote in thisGatra.notes:
            if thisNote.gong:
                gongTally[thisNote.pitch] += 1
            allTally[thisNote.pitch] += 1
            
                

print gongTally
print allTally