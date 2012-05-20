import cleanup
import cPickle as pickle
import random, math, os ,sys

### should return a dictionary mapping words to their document frequency
def buildCorpus(Dir) :
    dict ={}
    size = 0
    for Class in os.listdir(Dir):
        dir=os.path.join(Dir,Class)
        fileList=os.listdir(dir)
        size += len(fileList)
        for file in fileList:
            path=os.path.join(dir,file)
            data=open(path,'r').read()
            contents = cleanup.filterStopwords(data.split())
            contents = cleanup.stripPunctuation(contents)
            for word in set(contents) :
                try:
                    dict[word] += 1
                except:
                    dict[word] = 1
    pickle.dump(dict, open('dictionary','w')) 
    return size, dict   
    
### return a number between 0 and 1 depending on the similarity of the two pages.
def cosineSimilarity(page1, page2) :

    numerator = sum([page1[word] * page2[word] for word in page1 if word in page2])
    denominator = math.sqrt(sum([page1[word] * page1[word] for word in page1])) * math.sqrt(sum([page2[word] * page2[word] for word in page2])) 
    if numerator == 0: numerator = 1
    if denominator== 0:denominator =1
    result = float(numerator / denominator)
    return result


if __name__ == '__main__' :
    print buildCorpus("6NewsGroups")