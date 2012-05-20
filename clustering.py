import cPickle as pickle
import re, string, urllib
import clusters, math, random, os, cleanup

class document:
    def __init__(self,fname,cname,cont):
        self.filename=fname
        self.classname=cname
        self.newname= None
        self.contents=cont
        self.tfidfscores={}
        
    def __repr__(self):
        return self.filename
    
    def frequency(self, wordlist):
        wf ={}
        for word in wordlist:
            try:
                wf[word] += 1
            except:
                wf[word] = 1    
        return wf
        
    ### documentFrequencies is a dictionary containing all document frequencies
    def computeTFIDF(self, documentFrequencies, corpusSize=81) :
        contents = cleanup.filterStopwords(self.contents)
        contents = cleanup.stripPunctuation(contents)
        scoredWords = self.frequency(contents)
        for word in scoredWords :
            if word in documentFrequencies :
                scoredWords[word] = scoredWords[word] * math.log(corpusSize / documentFrequencies[word])
            else :
                scoredWords[word] = scoredWords[word] * math.log(corpusSize)
        self.tfidfscores = scoredWords    


class cluster:
    def __init__(self,fname):
        self.documents=fname
        self.classname=None
        self.center={}
        
    ###For each cluster compute new centers
    def computeNewCenters(self):
        allwords = []
        for document in self.documents:
            allwords.extend(document.contents)
        common = set(allwords)
        temptfidf = {}
        for word in common:
            
            totalscore = 0
            count =0
            score = 0
            for document in self.documents:
                if word in document.contents:
                    totalscore += document.tfidfscores[word]
                    count +=1
            score = totalscore/count
            temptfidf[word] = score
        self.center = temptfidf
            
    ### For each cluster compute name based on majority of documents.         
    def setClassName(self):
        list = [document.classname for document in self.documents]
        items = set(list)
        cos =[(1, 'alt.atheism')]
        for each in items:
            cos.extend([(list.count(each), each)])
        cos.sort()
        print cos
        self.classname= cos[-1][1]
             
        
    
class clustering:
     def __init__(self):
         self.alldocuments= {}
         self.clusters={}
     ## set up all the documents. Corpus is read.
     def setupdocuments(self,Dir):
         size = 0
         corpusfile = open('dictionary', 'r')
         corpus = pickle.load(corpusfile)
         for Class in os.listdir(Dir):
             dir=os.path.join(Dir,Class)
             fileList=os.listdir(dir)
             size += len(fileList)
             for file in fileList:
                path=os.path.join(dir,file)
                try :
                    data=open(path,'r').read()
                    contents = cleanup.filterStopwords(data.split())
                    contents = cleanup.stripPunctuation(contents)
                    d = document(file,Class,contents)
                    d.computeTFIDF(corpus)
                    self.alldocuments[d] = 1
                except :
                    pass
      
     ### pick k random clusters.           
     def pickRandomCenter(self, k):
         for i in range(0,k):
             d = self.alldocuments.keys()[random.randrange(1, len(self.alldocuments.keys()))]
             c= cluster([d])
             c.center = d.tfidfscores
             c.classname = d.classname
             self.clusters[c] = 1
             
    ### one iteration goes through all documents and classifies them.       
     def classifyone(self): 
         for document in self.alldocuments:
             cosines = []
             for clust in self.clusters:
                 cosines.extend([(clusters.cosineSimilarity(clust.center,document.tfidfscores), clust)])
             cosines.sort()
             document.newname= cosines[-1][1].classname
             cosines[-1][1].documents.extend([document]) 
             
             
     def classification(self):
         for each in self.clusters:
             each.documents =[]       
         self.classifyone()
         for each in self.clusters:
             each.computeNewCenters()
             each.setClassName()
             
         
     ### Compute the k-means algorithm. Change the number from 10 to increase
     ### the number of iterations. 
     def KmeansClustering(self, k):
         self.pickRandomCenter(k) 
         for i in range(0,10):
             print i
             self.classification()
         self.fMeasure()
         
     
     def fMeasure(self):
         print '____________________F-MEARURE_____________________________\n'
         for eachCluster in self.clusters.keys():
            allClasses=[eachDocument.newname for eachDocument in self.alldocuments if eachDocument.newname==eachCluster.classname]
            clusterDocs=[(allClasses.count(each),each) for each in set(allClasses)]
            clusterDocs.sort()
            num= clusterDocs[-1][0]
            name=clusterDocs[-1][1]
            precision=float(num)/sum([each[0] for each in clusterDocs])
            accuracy=float(num)/len([eachDoc for eachDoc in self.alldocuments if eachDoc.classname==name])
            #calculate fmeasure
            fm=accuracy*precision/(accuracy+precision)
            print 'Cluster ',eachCluster.classname,'--->',name,'     ',fm
            
           
            
### Name of the directory is 6NewsGroups. And 6 is the K.
### Feel free to change if you are testing with you documents and k.                  
if __name__ == '__main__' :
    compute = clustering()
    compute.setupdocuments("6NewsGroups")
    compute.KmeansClustering(6)

