# ybc module

import string
import os
import re
import sys

pitchCodesIn = ['1','2','3','4','5','6','7','q','w','e','r','t','y','u','!','@','#','\$','%','\^','&',]
pitchCodesOut = [' b1 ',' b2 ',' b3 ',' b4 ',' b5 ',' b6 ',' b7 ',' a1 ',' a2 ',' a3 ',' a4 ',' a5 ',' a6 ',' 7a ',' c1 ',' c2 ',' c3 ',' c4 ',' c5 ',' c6 ',' c7 ']

ybcCorpus = list()  # list of ybcBalungan instances

class ybcBalungan:
    def __init__(self, filename):
        self.filename = filename
        self.shortname = re.sub('/.*/(.*).txt','\g<1>',filename)
        self.gatras = list() # list of ybcGatra instances

class ybcGatra:
    def __init__(self):
        self.notes = list() # list of ybcNote instances
        
class ybcNote:                # class for balungan notes
    def __init__(self, pitch, beat):
    
        # pitch and beat must be identified
        self.pitch = pitch
        self.beat = beat
        
        # set defaults for other variables
        self.gong = False
        self.nong = False
        self.pul = False
        self.beatOffset = 0
        
    def __str__(self):
        return 'pitch = {0}, beat = {1}, gong = {2}, nong = {3}, pul = {4}'.format(self.pitch, self.beat, self.gong, self.nong, self.pul)

corpusRoot = '/Users/iq2/research/corpus/gamelan/sources/'

corpusDirs = [
#    'slendro/manyura/ladrang/',
#    'slendro/nem/ladrang/',
    'slendro/sanga/ladrang/'
]

corpusFiles = []
for theDir in corpusDirs:
    thePath = corpusRoot + theDir + 'txt/'
    corpusFiles.extend( [ thePath + f for f in os.listdir(corpusRoot + theDir + 'txt/') ] )
    

for theFile in corpusFiles:

    if theFile[-16:] == 'Sala Minulya.txt': continue # this file has a problem

    thisBalungan = ybcBalungan(theFile)
    f = open(theFile, 'r')
    for l in f:
        l = l.strip()
        l = re.sub('\\t\\t','\\t',l)   # get rid of double tabs, assuming they're meaningless
        l = re.sub('\\t\\t','\\t',l)   # do it again in case there were any triple tabs
        l = re.sub('\\[','',l)     # get rid of brackets until we know what to do with them
        l = re.sub('\\]','',l)
        l = re.sub('o ','',l)     # get rid of 'o' which represents a segno-type star in Kepatihan
        l = re.sub('o','',l)     # get rid of 'o' which represents a segno-type star in Kepatihan
        l = re.sub('\\\\','',l)     # get rid of '\' which represents a segno-type star in Kepatihan


        
        if len(l) == 0: continue
        m = re.search('<(.*)>', l)
#         print l
        if m:      # m is True if the current line consists of a <tag in angle brackets>
             pass  # we'll just ignore it for now
#            print m.groups(1)   # TK: use this metadata
        else:    # we've got plain data
#             print "parsing", l
            gatras = l.split('\t')   # split the current line on tab characters (which separate gatras)
            
            for g in gatras:

                # beats within gatra are separated by spaces -- split on spaces and clean up
                gs = string.rstrip(g).split(' ')
                i = 0
                while i < len(gs):  
                    
                    # three successive spaces in the input file is interpreted as a single blank beat
                    # split will have parsed three successive spaces into two successive null strings
                    if i+1 < len(gs) and gs[i] == '' and gs[i+1] == '': 
                        gs.pop(i+1) # delete the second null string
                        
                    else:
                        i += 1

                # die if there are more than four beats in the gatra
                if len(gs) > 4: 
                    sys.exit('gatra with more than four beats in ' + theFile + ': ' + str(gs) + '>'+l)
                    
                # if we have fewer than four beats, assume they are at the end of the gatra
                if len(gs) < 4:
                    for j in range(4-len(gs)):
                        gs[:0] = [' '] # insert a space before the first item in gs
                
                # now we're ready to create a ybcGatra instance for this gatra
                thisGatra = ybcGatra()
                        
                # parse pitch characters, adding spaces before and after
                old = str(gs)
                for beat in range(len(gs)):


                    noteCount = 0
                    # we use two matching lists (pitchCodesIn and -Out) so we can go through in
                    # the right order; digits need to get translated first because we use them
                    # in the output as well as the input
                    for j in range(len(pitchCodesIn)):
                        (newtext, subs) = re.subn(pitchCodesIn[j], pitchCodesOut[j], gs[beat])
                        gs[beat] = newtext
                        noteCount += subs
                    
#                   print noteCount, gs[i], gs, old
                    # get rid of any extra spaces we just made
                    gs[beat] = re.sub('^ ','',gs[beat])  # eliminate leading spaces
                    gs[beat] = re.sub(' $','',gs[beat])  # eliminate trailing spaces
                    gs[beat] = re.sub('  ',' ',gs[beat]) # consolidate double spaces
                    
                    beatContents = string.rsplit(gs[beat], ' ')
                    
                    # trivial case: a rest only
                    if noteCount == 0:
                        theNote = ybcNote('',beat)
                        
                    # simplest non-trivial case: one note in the beat
                    elif noteCount == 1:
                        if len(beatContents) == 1:
                            thisNote = ybcNote(beatContents[0], beat)
                        elif len(beatContents) == 2:
                            # the first item in beatContents is a gong marker
                            thisNote = ybcNote(beatContents[1], beat)
                            if re.search('n',beatContents[0]): 
                                thisNote.nong = True
                            if re.search('p',beatContents[0]): 
                                thisNote.pul = True
                            if re.search('g',beatContents[0]): 
                                thisNote.gong = True
                        else:
                            sys.exit('syntax error in '+filename+': '+l)
                        thisGatra.notes.append(thisNote)
                            
                    # with two notes in the beat we assume they're equal
                    elif noteCount == 2:
                        thisNote = ybcNote('',beat)
                        while beatContents != []:
                            if beatContents[0][0] not in string.digits:
                                if re.search('n',beatContents[0]): 
                                    thisNote.nong = True
                                if re.search('p',beatContents[0]): 
                                    thisNote.pul = True
                                if re.search('g',beatContents[0]): 
                                    thisNote.gong = True
                                beatContents.pop(0)
                                continue
                            else:
                                thisNote.pitch = beatContents[0]
                                thisGatra.notes.append(thisNote)
                                if len(beatContents) > 1: 
                                    thisNote = ybcNote('',beat + 0.5)
                                beatContents.pop(0)
                                continue
                    
                    # with more than two notes we only look at the first note                
                    else: 
                        print 'WARNING: Ignoring all but first note in a beat with more than 2 subdivisions.'
                        print 'File: '+thisBalungan.filename
                        thisNote = ybcNote('',beat)
                        if beatContents[0][0] not in string.digits:
                            if re.search('n',beatContents[0]): 
                                thisNote.nong = True
                            if re.search('p',beatContents[0]): 
                                thisNote.pul = True
                            if re.search('g',beatContents[0]): 
                                thisNote.gong = True
                        else:
                            thisNote.pitch = beatContents[0]
                        thisGatra.notes.append(thisNote)
                                    

                # now add theGatra to theBalungan
                thisBalungan.gatras.append(thisGatra)
                 
    # add thisBalungan to the corpus
    ybcCorpus.append(thisBalungan)