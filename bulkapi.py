__author__ = 'Region Star'
import json

def get_jsondata_from_id(stype, _id):
    filepath = 'bulk-data/%s/%s.json' % (stype, str(_id))
    try:
        with open(filepath) as f:
            data = json.load(f)
        return data
    except Exception as e:
        print('Load JSON ERROR: ', str(e))
    return None


def get_jsondata_from_url(url):
    tmparr = url.split('/')
    tmpid = tmparr[-1]
    if tmpid == '':
        tmpid = tmparr[-2]
        tmptype = tmparr[-3]
    else:
        tmptype = tmparr[-2]

    return get_jsondata_from_id(tmptype, tmpid)
