# ybc module

import string
import os
import re
import sys

'''
TO DO:
find out from Sarah if the kenong plays with the gong even when it isn't notated. (Maho seems to say yes) -- in general, how much can we trust the notation when it comes to nong/pul
are there cases where the nong/pul plays a different pitch than the balungan pitch?
'''

pitchCodesIn = ['1','2','3','4','5','6','7','q','w','e','r','t','y','u','!','@','#','\$','%','\^','&','\.']
pitchCodesOut = ['b1 ','b2 ','b3 ','b4 ','b5 ','b6 ','b7 ','a1 ','a2 ','a3 ','a4 ','a5 ','a6 ','7a ','c1 ','c2 ','c3 ','c4 ','c5 ','c6 ','c7 ','. ']

class ybcBalungan:
    def __init__(self, filename):
        self.filename = filename
        self.shortname = re.sub('/.*/(.*).txt','\g<1>',filename)
        self.gatras = list() # FLAT list of ybcGatra instances (all sections together)
        self.sections = list() # list of ybcSection instances (includes another copy of gatra list)
        self.scale = ''
        self.mode = ''

class ybcSection:
    def __init__(self):
        self.gatras = list() # list of ybcGatra instances
        self.name = ''

class ybcGatra:
    def __init__(self):
        self.notes = list() # list of ybcNote instances
        
    def __str__(self):
        output = ''
        for n in self.notes: output += n.__str__() + '\n'
        return output
        
class ybcNote:                # class for balungan notes
    def __init__(self, pitch='', beat='-1', encoded=''):
        global prevPitch
    
        # set defaults 
        self.beat = beat
        self.restDot = False
        self.gong = False
        self.nong = False
        self.pul = False
        
        if encoded == '':
            self.pitch = pitch
        else:
            while encoded[0] in 'gnp':
                if encoded[0] == 'g':
                    self.gong = True
                if encoded[0] == 'n':
                    self.nong = True
                if encoded[0] == 'p':
                    self.pul = True
                encoded = encoded[1:]
            if encoded == '.':
                self.pitch = prevPitch
                self.restDot = True
            else:
                self.pitch = encoded
            prevPitch = self.pitch
            
        
    def __str__(self):
        return 'pitch = {:2} | beat = {:<5} | rest = {:1} | gong = {:1} | nong = {:1} | pul = {:1}'.format(self.pitch, self.beat, self.restDot, self.gong, self.nong, self.pul)

class ybcCorpus:
    def __init__(self, ybcPathname):
    
        global prevPitch

        self.balungans = list()
        
        corpusDirs = [
            'slendro/manyura/ladrang/',
            'slendro/nem/ladrang/',
            'slendro/sanga/ladrang/'
        ]

        corpusFiles = []
        for theDir in corpusDirs:
            thePath = ybcPathname + '/corpus/' + theDir + 'txt/'
            corpusFiles.extend( [ thePath + f for f in os.listdir(thePath) ] )
    

        for theFile in corpusFiles:
        
            if theFile[-3:] != 'txt': continue

            thisBalungan = ybcBalungan(theFile)
            thisSection = ybcSection()
            thisSection.name = 'unnamed'
            thisBalungan.sections.append(thisSection)
            
            prevPitch = ''

            f = open(theFile, 'r')
            for l in f:
                l = l.strip()
                
                # treat blank lines as section breaks
        
                if len(l) == 0: 
                    l = '<S>'
                tag = re.search('<(.*)>', l)
                if tag:      # m is True if the current line consists of a <tag in angle brackets>
                    metadata = string.rsplit(tag.groups(1)[0],' ')   # TK: use this metadata
                    if metadata[0] == 'P':
                        thisBalungan.mode = metadata[1]
                    if metadata[0] == 'L':
                        thisBalungan.scale = metadata[1]
                    if metadata[0] == 'S':
                        if len(metadata) == 1: metadata.append('unnamed')
                        if len(thisBalungan.gatras) > 0:
                            thisSection = ybcSection()
                            thisBalungan.sections.append(thisSection)
                        thisSection.name = ' '.join(metadata[1:])

                else:    # we've got plain data

                    # do some basic cleanup
                    l = re.sub('\\t\\t','\\t',l)   # get rid of double tabs, assuming they're meaningless
                    l = re.sub('\\t\\t','\\t',l)   # do it again in case there were any triple tabs
                    l = re.sub('\\[','',l)     # get rid of brackets until we know what to do with them
                    l = re.sub('\\]','',l)
                    l = re.sub('o ','',l)     # get rid of 'o' which represents a segno-type star in Kepatihan
                    l = re.sub('o','',l)     # get rid of 'o' which represents a segno-type star in Kepatihan
                    l = re.sub('\\\\','',l)     # get rid of '\' which represents a segno-type star in Kepatihan


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
                        for beat in range(len(gs)):


                            noteCount = 0
                            # we use two matching lists (pitchCodesIn and -Out) so we can go through in
                            # the right order; digits need to get translated first because we use them
                            # in the output as well as the input
                            for j in range(len(pitchCodesIn)):
                                (newtext, subs) = re.subn(pitchCodesIn[j], pitchCodesOut[j], gs[beat])
                                gs[beat] = newtext
                                noteCount += subs
                            gs[beat] = re.sub('_','',gs[beat]) # underscores represent empty spaces (real rests)
                            gs[beat] = re.sub('j','',gs[beat]) # get rid of stray j's from earlier encoding system
                            gs[beat] = re.sub('k','',gs[beat]) # get rid of stray k's from earlier encoding system
                            gs[beat] = re.sub(' $','',gs[beat])  # eliminate trailing space
                            
                            # this next thing is a kludge - G is a mark for 'gong suwukan'
                            gs[beat] = re.sub('G','',gs[beat]) # get rid of stray k's from earlier encoding system
                            

                            beatContents = string.rsplit(gs[beat], ' ')
                            
                            # trivial case: a rest only
                            if noteCount == 0:
                                theNote = ybcNote('',beat)
                        
                            # simplest non-trivial case: one note in the beat
                            elif noteCount == 1:
                                thisGatra.notes.append(ybcNote(beat = beat, encoded=beatContents[0]))
                            
                            # with two or four notes in the beat we assume they're equal
                            elif noteCount == 2:
                                thisGatra.notes.append(ybcNote(beat = beat, encoded=beatContents[0]))
                                thisGatra.notes.append(ybcNote(beat = beat+0.5, encoded=beatContents[1]))
                    
                            elif noteCount == 4:
                                thisGatra.notes.append(ybcNote(beat = beat, encoded=beatContents[0]))
                                thisGatra.notes.append(ybcNote(beat = beat+0.25, encoded=beatContents[1]))
                                thisGatra.notes.append(ybcNote(beat = beat+0.5, encoded=beatContents[2]))
                                thisGatra.notes.append(ybcNote(beat = beat+0.75, encoded=beatContents[3]))
                    
                            # with three notes the first character must specify the rhythm
                            elif noteCount == 3: 
                                if beatContents[0][0] not in 'AD':
                                    sys.stderr.write('WARNING: Ignoring all but first note in a beat with 3 subdivisions and no rhythm specifier.\n')
                                    sys.stderr.write('File: '+thisBalungan.filename+'\n')
                                    thisGatra.notes.append(ybcNote(beat = beat, encoded=beatContents[0]))
                                else:
                                    if beatContents[0][0] == 'D':  # D is for dactyl
                                        beatContents[0] = beatContents[0][1:]
                                        thisGatra.notes.append(ybcNote(beat = beat, encoded=beatContents[0]))
                                        thisGatra.notes.append(ybcNote(beat = beat+0.5, encoded=beatContents[1]))
                                        thisGatra.notes.append(ybcNote(beat = beat+0.75, encoded=beatContents[2]))
                                    elif beatContents[0][0] == 'A':  # A is for anapest
                                        beatContents[0] = beatContents[0][1:]
                                        thisGatra.notes.append(ybcNote(beat = beat, encoded=beatContents[0]))
                                        thisGatra.notes.append(ybcNote(beat = beat+0.25, encoded=beatContents[1]))
                                        thisGatra.notes.append(ybcNote(beat = beat+0.5, encoded=beatContents[2]))

                        # now add theGatra to theBalungan and theSection
                        thisBalungan.gatras.append(thisGatra)
                        thisSection.gatras.append(thisGatra)
                 
            # add thisBalungan to the corpus
            self.balungans.append(thisBalungan)