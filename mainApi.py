# -*- coding: utf-8 -*-

from filterApi import SpamFilter
from flask import Flask
from flask.ext.restful import Api
from config import configs
import flask_restful.representations.json

flask_restful.representations.json.settings['indent'] = 4

app = Flask(__name__)
api = Api(app)

# 注册API服务
api.add_resource(SpamFilter, '/api/spamfilter')

if __name__ == '__main__':
    app.run(configs['bind_addr'], configs['bind_port'], threaded=True)