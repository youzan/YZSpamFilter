# -*- coding: utf-8 -*-

configs = {
           'bind_addr': '0.0.0.0',  #服务绑定地址
           'bind_port': 5060,       #服务绑定端口
           'threshold': 83,          #过滤阈值
           'stopwords_file':'stopwords_common.txt',  #停止词文件
           'classify_model':'filter.pickle',         #过滤模型
           'ham_file':'ham.txt',                     #正常信息
           'spam_file':'spam.txt',                   #垃圾信息
           'train_rate':0.5                          #正常、垃圾信息中用于训练的信息比例（范围0到1）
          }