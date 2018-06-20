__author__ = 'Region Star'

import os
import sys


class BaseConfig(object):
    DEBUG = True
    CSV_ITEM_LIMIT = 99999999
    OPINION_LIMIT = 1000

    IS_LOCAL_DB = True
    # MONGODB_HOSTNAME = 'iad2-c4-0.mongo.objectrocket.com:52553,iad2-c4-1.mongo.objectrocket.com:52553,iad2-c4-2.mongo.objectrocket.com:52553'
    # MONGODB_USER = 'user'
    # MONGODB_PWD = 'pwd'
    # MONGODB_DBNAME = 'ExemptV1Dev'
    # MONGODB_COLLECTION = 'TEST'

    MONGODB_HOSTNAME = 'localhost:27017'
    MONGODB_USER = ''
    MONGODB_PWD = ''
    MONGODB_DBNAME = 'ExemptDB'
    MONGODB_COLLECTION = 'ExemtCases'

    CITATIONS_CSV_FILEPATH = 'bulk-data/citations/citations.all.csv'
    # CITATIONS_CSV_FILEPATH = 'example.csv'