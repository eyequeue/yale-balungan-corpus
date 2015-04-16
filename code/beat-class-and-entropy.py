import kl
import ybc
import collections

c = ybc.ybcCorpus('/Users/iq2/research/corpus/gamelan/yale-balungan-corpus/')

d = dict()
for bc in ['w','x','y','z']: d[bc] = collections.Counter()

for m in ['manyura','sanga','nem']:
	print m
	for b in c.balungans:
		if b.mode != m: continue
		for s in b.sections:
			for (i,g) in enumerate(s.gatras):
				for n in g.notes:
					if n.beat == 3:
						for bc in ['w','x','y','z']:
							try:
								if bc == 'z':
									p1 = g.getNoteAtBeat(2).pitch
								elif bc == 'y':
									p1 = g.getNoteAtBeat(1).pitch
								elif bc == 'x':
									p1 = g.getNoteAtBeat(0).pitch
								elif bc == 'w':
									p1 = s.gatras[i-1].getNoteAtBeat(3).pitch
								t = tuple( [p1 ,n.pitch] )
								d[bc][t] += 1
							except:
								pass

	print kl.ConditionalEntropy(d['w'])
	print kl.ConditionalEntropy(d['x'])
	print kl.ConditionalEntropy(d['y'])
	print kl.ConditionalEntropy(d['z'])
		