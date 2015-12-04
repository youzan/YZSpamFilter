# -*- coding: utf-8 -*-

import os
import sys
import random
import jieba
from utils import ClearAndSegment

trainPos = "trainPos.txt"
trainNeg = "trainNeg.txt"
testPos = "testPos.txt"
testNeg = "testNeg.txt"

def createTrainAndTestData(strpos, strneg, trainRate, stopWords):

    fpos = open(strpos)
    totalPos = fpos.readlines()
    fneg = open(strneg)
    totalNeg = fneg.readlines()
    #trainRate = 0.9999
    trainPosNum = int(trainRate * len(totalPos))
    trainNegNum = int(trainRate * len(totalNeg))
   
    trainPosIndex = random.sample(range(len(totalPos)),trainPosNum)
    trainNegIndex = random.sample(range(len(totalNeg)),trainNegNum)

    trainPosArray = []
    testPosArray = []
    trainNegArray = []
    testNegArray = []

    fstop = open(stopWords)
    totalStop = fstop.readlines()
    stops = []
    for s in totalStop:
        s = s.strip()
        stops.append(s)

    index = 0
    for i in range(len(totalPos)):
        str = totalPos[i]
        str = str.strip()
        if str == '':
            continue
        #print str
        str = ClearAndSegment(str)
        str = [word for word in str if word not in stops]
        str = '/'.join(str)
        str = str + '\n'
        if not str.strip():
            continue
        index +=1
        if index%1000 == 0:
            print 'Adding positive data: %d' % (index)

        if i in trainPosIndex:
            trainPosArray.append(str)
        else:
            testPosArray.append(str)
    print '\n'
    index = 0
    for i in range(len(totalNeg)):
        str = totalNeg[i]
        str = str.strip()
        if str == '':
            continue
        str = ClearAndSegment(str)
        str = [word for word in str if word not in stops]
        str = '/'.join(str)
        str = str + '\n'
        if not str.strip():
            continue
        index +=1
        if index%1000 == 0:
            print 'Adding negative data: %d' % (index)

        if i in trainNegIndex:
            trainNegArray.append(str)
        else:
            testNegArray.append(str)
    print '\n'
    print "len of trainPos is %d\n" % (len(trainPosArray))
    print "len of trainNeg is %d\n" % (len(trainNegArray))
    print "len of testPos is %d\n" % (len(testPosArray))
    print "len of testNeg is %d\n" % (len(testNegArray))

    ftrainPos = open(trainPos, "w")
    ftrainNeg = open(trainNeg, "w")
    ftestPos = open(testPos, "w")
    ftestNeg = open(testNeg, "w")
    
    #for ele in trainPosArray:
    #    ftrainPos.write(ele)
    ftrainPos.writelines(trainPosArray)
    ftrainNeg.writelines(trainNegArray)
    ftestPos.writelines(testPosArray)
    ftestNeg.writelines(testNegArray)
    
    fpos.close()
    fneg.close()
    
    ftrainPos.close()
    ftestPos.close()
    ftrainNeg.close()
    ftestNeg.close()
    fstop.close()

if __name__ == "__main__":

    """
    usage: python createTrainAndTestData.py ham.txt spam.txt 0.5 stopwords.txt

    """

    reload(sys)
    sys.setdefaultencoding('utf-8')
    if len(sys.argv) < 3:
        print "输入的参数过少"
        sys.exit()
    strpos = sys.argv[1]
    strneg = sys.argv[2]

    if not os.path.exists(strpos):
        print "ERROR: need ham file"
        sys.exit(-1)

    if not os.path.exists(strneg):
        print "ERROR: need spam file"
        sys.exit(-1)

    trainRate = 0.5
    stopWords = 'stopwords_common.txt'

    if len(sys.argv) > 3:
        trainRate = float(sys.argv[3])

    if len(sys.argv) > 4:
        stopWords = sys.argv[4]

    createTrainAndTestData(strpos, strneg, trainRate, stopWords)
     
