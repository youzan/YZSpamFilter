#coding=utf-8
import os
import sys
import pickle

from classifier import Algorithm

classifyname = "filter.pickle"

class filter:
    def __init__(self, Algorithm):
        self.Algorithm = Algorithm
        self.tar = 0.0
        self.trr = 0.0
        self.accuracy = 0.0
        self.hashset = set()

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    ##############################
    # 1.train or load model
    ##############################
    if not os.path.exists(classifyname):
        print "you should have a model first"
        exit(-1)

    else:
        with open(classifyname, 'rb') as file:
            f = filter(Algorithm)
            t = pickle.load(file)
            f.Algorithm.loadmodel(t)
            file.close()
        ##############################
        # 1.错误的将正常信息当做垃圾信息（误抓取）
        ##############################
        FalseRejectstr = ['新开','店铺','买','送','欢迎','大家' ,'关顾']
        f.Algorithm.discover(FalseRejectstr, True)
        f.Algorithm.cover(FalseRejectstr, False)

        ##############################
        # 1.错误的将垃圾信息当做正常信息（漏抓取）
        ##############################
        FalseAcceptstr = ['官网','诚招','手机','电脑','打字员','日入','百百']
        f.Algorithm.cover(FalseAcceptstr, True)
        file = open(classifyname, 'wb')
        t = f.Algorithm.getmodel()
        pickle.dump(t, file)
        file.close()


