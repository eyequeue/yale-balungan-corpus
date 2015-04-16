# provides support for Kullback-Leibler divergence

import math
import copy
import collections

def isFloat(x):
    try:
        y = float(x)
        return True
    except:
        return False

# KL takes two dictionaries (assumed to be tallies or probability distributions) 
# and computes their Kullback-Leibler divergence.  Any dictionary entries whose
# values can't be interpreted as floating-point numbers or integers are ignored,
# as are entries whose key is 'total'.  EVERYTHING ELSE COUNTS, so it's your
# responsibility to make sure that there isn't any stray stuff in your dictionaries
# that will screw up the computation.
#
# You should use 'flat' dictionaries (i.e. not dictionaries of dictionaries) for this.
#
# Instances of the collections.Counter class can also be used instead of dictionaries.

def KL (d1, d2):

    dict1 = copy.copy(d1)
    dict2 = copy.copy(d2)
        
    for dict in [dict1,dict2]:

        # delete 'total' keys if they exist
        if 'total' in dict: del dict['total']
    
        # delete any value that can't be interpreted as a float
        for k in dict:
            if not isFloat(dict[k]):
                del dict[k]

        # normalize
        total = 0.
        for k in dict:
            total += float(dict[k])
        for k in dict:
            dict[k] = dict[k]/total
        

    # put all keys of dict1 into dict2 and vice versa
    
    for k in dict1:
        if k not in dict2:
            dict2[k] = 0 
    for k in dict2:
        if k not in dict1:
            dict1[k] = 0 
            
    # smooth (add .01) and renormalize
    
    for dict in [dict1, dict2]:
        for k in dict:
            dict[k] = ((dict[k] + .01) / (1. + (len(dict) * .01)))
    # compute KL divergence
    
    kld = 0
    for k in dict1:
        kld += dict1[k] * math.log(dict1[k]/dict2[k], 2)
        
    return kld
  
def ConditionalEntropy (d):  # d is a dictionary of tuples

    dict1 = collections.Counter()
    dict2 = collections.Counter()

    for t in d:
        dict1[t[0]] += d[t]
        dict2[t[1]] += d[t]
    
    H = 0
    for i in dict1:
        for j in dict2: 
                s = sum(dict2.values())
                p_i = 1.*dict1[i]/sum(dict1.values())
                p_j = 1.*dict2[j]/sum(dict2.values())
                p_joint = 1.*d[tuple([i,j])]/s
                if p_joint == 0: continue
                H += p_joint * math.log( p_i / p_joint )
  #              pass
    return H
    print dict1, dict2
