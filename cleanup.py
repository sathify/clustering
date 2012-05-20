'''
Created on Nov 17, 2010

@author: satheesh
'''

### Strips html tags
def regexStrip(string) :
    st = re.compile('<.*?>', re.DOTALL)
    return re.sub(st,'',string)

### Strips punctuation
def stripPunctuation(string):
    return [word for word in string if word.isalpha()]


### Filters the stop words
def filterStopwords(wordlist) :
    stopwords = ['I', 'a', 'an', 'as', 'at', 'by', 'he', 'his', 'me', 
            'or', 'thou', 'us', 'who', 'against', 'amid', 'amidst','among', 'amongst',
            'and', 'anybody', 'anyone', 'because', 'beside', 'circa',
            'despite', 'during', 'everybody', 'everyone', 'for', 'from', 'her',
            'hers', 'herself', 'him', 'himself', 'hisself', 'idem', 'if',
            'into', 'it', 'its', 'itself', 'myself', 'nor', 'of', 'oneself',
            'onto', 'our', 'ourself', 'ourselves', 'per', 'she', 'since',
            'than', 'that', 'the', 'thee', 'theirs', 'them', 'themselves',
            'they', 'thine', 'this', 'thyself', 'to', 'tother', 'toward',
            'towards', 'unless', 'until', 'upon', 'versus', 'via', 'we',
            'what', 'whatall', 'whereas', 'which', 'whichever', 'whichsoever',
            'whoever', 'whom', 'whomever', 'whomso', 'whomsoever', 'whose',
            'whosoever', 'with', 'without', 'ye', 'you', 'you-all', 'yours',
            'yourself', 'yourselves', 'aboard', 'about', 'above', 'across',
            'after', 'all', 'along', 'alongside', 'although', 'another',
            'anti', 'any', 'anything', 'around', 'astride', 'aught', 'bar',
            'barring', 'before', 'behind', 'below', 'beneath', 'besides',
            'between', 'beyond', 'both', 'but', 'concerning', 'considering',
            'down', 'each', 'either', 'enough', 'except', 'excepting',
            'excluding', 'few', 'fewer', 'following', 'ilk', 'in',
            'including', 'inside', 'like', 'many', 'mine', 'minus', 'more',
            'most', 'naught', 'near', 'neither', 'nobody', 'none', 'nothing',
            'notwithstanding', 'off', 'on', 'opposite', 'other', 'otherwise',
            'outside', 'over', 'own', 'past', 'pending', 'plus', 'regarding',
            'round', 'save', 'self', 'several', 'so', 'some', 'somebody',
            'someone', 'something', 'somewhat', 'such', 'suchlike', 'sundry',
            'there', 'though', 'through', 'throughout', 'till', 'twain',
            'under', 'underneath', 'unlike', 'up', 'various', 'vis-a-vis',
            'whatever', 'whatsoever', 'when', 'wherewith', 'wherewithal',
            'while', 'within', 'worth', 'yet', 'yon', 'yonder']
    return [word for word in wordlist if word not in stopwords]


