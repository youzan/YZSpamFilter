#coding=utf-8
import os
import sys
import pickle

from classifier import Algorithm
from utils import ClearAndSegment
trainPos = "trainPos.txt"
trainNeg = "trainNeg.txt"
testPos = "testPos.txt"
testNeg = "testNeg.txt"

posScore = "posScore.txt"
negScore = "negScore.txt"

classifyname = "filter.pickle"

class filter:

    def __init__(self, Algorithm):
        self.Algorithm = Algorithm
        self.tar = 0.0
        self.trr = 0.0
        self.accuracy = 0.0
        self.hashset = set()

    def train(self):
        fTrainPos = open(trainPos)
        fTrainNeg = open(trainNeg)
        trainPosArray = fTrainPos.readlines()
        trainNegArray = fTrainNeg.readlines()

        totalPos = len(trainPosArray)
        totalNeg = len(trainNegArray)
        realPos = 0
        realNeg = 0
        for pos in trainPosArray:

            hashvalue = hash(pos)
            if hash(pos) not in self.hashset:
                self.hashset.add(hashvalue)
            else:
                continue
            realPos += 1
            pos = pos.strip('')
            pos = pos.split('/')
            is_spam = False
            self.Algorithm.cover(pos, is_spam)

        for neg in trainNegArray:

            hashvalue = hash(neg)
            if hashvalue not in self.hashset:
                self.hashset.add(hashvalue)
            else:
                continue

            realNeg += 1
            neg = neg.strip('')
            neg = neg.split('/')
            #neg = neg.strip('/')
            #neg = [word for word in neg]
            is_spam = True
            self.Algorithm.cover(neg, is_spam)

        print "Real Train Pos: %d, Total Train Pos:%d " % (realPos, totalPos)
        print "Real Train Neg: %d, Total Train Neg:%d " % (realNeg, totalNeg)

    def test(self, threshold):
        fPosScore = open(posScore, 'w')
        fNegScore = open(negScore, 'w')

        fTestPos = open(testPos)
        fTestNeg = open(testNeg)
        testPosArray = fTestPos.readlines()
        testNegArray = fTestNeg.readlines()

        totalPos = len(testPosArray)
        totalNeg = len(testNegArray)

        assert totalPos > 0
        assert totalNeg > 0

        print "Test Pos: %d" % (totalPos)
        print "Test Neg: %d" % (totalNeg)

        rightPos = 0
        rightNeg = 0

        for pos in testPosArray:
            pos = pos.strip('')
            pos = pos.split('/')
            #pos = pos.strip('/')
            #pos = [word for word in pos]
            score = self.Algorithm.predict(pos)
            #print score
            fPosScore.write("%d\n" % (score))

            if score > threshold:
                is_spam = True
            else:
                is_spam = False

            if is_spam==False:
                rightPos+=1
        fPosScore.close()

        for neg in testNegArray:
            neg = neg.strip('')
            neg = neg.split('/')
            #neg = neg.strip('/')
            #neg = [word for word in neg]
            score = self.Algorithm.predict(neg)
            fNegScore.write("%d\n" % (score))

            if score > threshold:
                is_spam = True
            else:
                is_spam = False

            if is_spam==True:
                rightNeg+=1
        fNegScore.close()

        self.tar = float(rightPos)/totalPos
        self.trr = float(rightNeg)/totalNeg
        self.accuracy = float(rightPos+rightNeg)/(totalPos+totalNeg)

    def singlejudge(self, wordlist):
        score = self.Algorithm.predict(wordlist)
        return score

if __name__ == '__main__':

    threshold = 83

    reload(sys)
    sys.setdefaultencoding('utf-8')

    ##############################
    # 1.train or load model
    ##############################
    if os.path.exists(classifyname):
        with open(classifyname, 'rb') as file:
            f = filter(Algorithm)
            t = pickle.load(file)
            f.Algorithm.loadmodel(t)
            file.close()

    else:
        f = filter(Algorithm)
        f.train()
        with open(classifyname, 'wb') as file:
            t = f.Algorithm.getmodel()
            pickle.dump(t, file)
            file.close()

    ##############################
    # 2.test
    ##############################
    f.test(threshold)
    print "tar = %f" % (f.tar)
    print "trr = %f" % (f.trr)
    print "accuracy = %f" % (f.accuracy)

    ##############################
    # 3.single judge
    ##############################
    stopWords = 'stopwords_common.txt'
    fstop = open(stopWords)
    totalStop = fstop.readlines()
    fstop.close()
    stops = []
    for s in totalStop:
        s = s.strip()
        stops.append(s)

    str = '赚钱test宝妈tes日赚学生兼职*.@打字员'
    print str
    liststr = ClearAndSegment(str)
    #print liststr
    liststr = [word.encode('UTF-8') for word in liststr if word not in stops]

    if f.singlejudge(liststr) > threshold:
        print 'WARNING: this is a spam message'
    else:
        print 'this message is harmless'

