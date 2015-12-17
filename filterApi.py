# -*- coding: utf-8 -*-

import os
import sys
import logging
from config import configs
from utils import ClearAndSegment, u
from flask.ext.restful import abort, Resource
from flask import request, make_response, jsonify
from classifier import Algorithm
from filter import filter
import pickle


reload(sys)
sys.setdefaultencoding('utf-8')

stopwords_file = configs['stopwords_file']
fstop = open(stopwords_file)
totalStop = fstop.readlines()
fstop.close()
stops = []
for s in totalStop:
    s = s.strip()
    stops.append(s)

threshold = configs['threshold']
classify_model = configs['classify_model']
if not os.path.exists(classify_model):
    print "ERROR: you should have a filter model"
    exit(-1)

with open(classify_model, 'rb') as file:
    f = filter(Algorithm)
    t = pickle.load(file)
    f.Algorithm.loadmodel(t)
    file.close()

class SpamFilter(Resource):

    """
      垃圾信息过滤服务

    """

    def get(self):
        if 'query' not in request.args:
            abort(404, message="parameter `query` doestn't exist")
        query = u(request.args['query'])
        #logging.debug("new query '%s'" % (query))
        liststr = ClearAndSegment(query)
        #print liststr
        liststr = [word.encode('UTF-8') for word in liststr if word not in stops]
        score = f.singlejudge(liststr)
        #print score
        body = {}
        if score > threshold:
            body = {'spam': 'True'}
        else:
            body = {'spam': 'False'}

        resp = make_response(jsonify(body))

        return resp
