# provides support for Kullback-Leibler divergence

import math
import copy

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
  