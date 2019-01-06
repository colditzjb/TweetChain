# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 20:05:32 2018

@author: colditzjb
"""
import sys
TweetLength = 280


def phraser(TextIn, style=None):
    while '  ' in TextIn:
        TextIn = TextIn.replace('  ',' ')
        
    MajorPunct = ['.','?','!']
    MinorPunct = [',',':',';','-']
    if style == 'minor':
        splits = MajorPunct + MinorPunct
    else:
        splits = MajorPunct
    tokens = TextIn.split(' ')
    t = 0
    phrases = ['']
    p = 0

    for token in tokens:
        if 'http' in token:
            if phrases[p] == '':
                phrases[p] = token
                phrases.append('')
                p += 1
            else:
                phrases.append(token)
                phrases.append('')
                p += 2
        else:
            phrases[p] = phrases[p]+ ' ' + token
            if token[-1] in splits: 
                phrases[p] = phrases[p].strip()
                phrases.append('')
                p += 1

        t += 1

    return phrases



def chunker(phrases, hashtags=[], tweetLen=TweetLength, linkLen=23):

    hashes = ''
    if len(hashtags) > 0:
        for hashtag in hashtags:
            hashes += (hashtag+' ')
        hashes = ' ' + hashes.strip() + ' '           

    LengthAllowed = tweetLen - len(hashes) - 5 #update this for 'i/n' convention

    # This creates an array of text length for each phrase
    # Links are handled so that they always append to the preceding phrase
    # Note: All Twitter links are 23 characters in length
    PhraseArray = []
    p = 0
    for phrase in phrases:
        if 'http' in phrase:
            PhraseArray[p-1] += (linkLen+1)
            PhraseArray.append(0)
        else:
            PhraseArray.append(len(phrase)+1)
        p += 1

    i = 0
    chunk = 0
    chunkLen = 0
    chunks = ['']
    for iLen in PhraseArray:
        if chunkLen > LengthAllowed:
            msg = ('Length over-run - revisit your sentence and try again!\n'+
            'Note: Character count may include trailing links (not printed):\n\n')
            sen = phrases[i-1]+'\n'
            stat = 'Length: '+str(PhraseArray[i-1]) 
            sys.exit(msg+sen+stat)
        
        if chunkLen + iLen <= LengthAllowed:
            chunkLen += iLen
            chunks[chunk] += (phrases[i]+' ')
            i += 1
            # If there is a link, cut it off there...
            if iLen == 0:
                chunk += 1
                chunkLen = 0
                chunks.append('')
        else:
            chunk += 1
            chunkLen = iLen
            chunks.append('')
            chunks[chunk] += (phrases[i]+' ')
            i += 1

    return chunks


def formatter(chunks, hashtags=[]):
    i = 1
    formatted = []
    
    hashes = ''
    if len(hashtags) > 0:
        for hashtag in hashtags:
            hashes += (hashtag+' ')
        hashes = ' ' + hashes.strip() + ' '
    else:
        hashes = ' '

    for chunk in chunks:
        stamp = str(i)+'/'+str(len(chunks))
        tokens = chunk.strip().split(' ')
        if 'http' in tokens[-1]:
            link = tokens[-1]
            formatted.append(' '.join(tokens[:-1])+hashes+stamp+' '+link)
        else:
            formatted.append(' '.join(tokens)+hashes+stamp)

        i += 1    
        
    return formatted



### This is where the magic happens...

dirin = './'
textin = 'test.txt'

TextBody = ''
with open(dirin+textin, 'r') as intext:
    for l in intext:
        TextBody = TextBody + ' ' + l.strip()
    TextBody = TextBody.strip()
        
hashtags = []

phrases = phraser(TextBody)
chunks = chunker(phrases, hashtags=hashtags)
tweets = formatter(chunks, hashtags=hashtags)

print('\nTWEETS:\n')
for t in tweets:
    print(str(len(t))+'\n'+t+'\n')
