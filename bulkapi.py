__author__ = 'Region Star'
import json


def get_jsondata_from_id(stype, _id):
    filepath = 'bulk-data/%s/%s.json' % (stype, str(_id))
    try:
        with open(filepath, encoding="utf8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print('Load JSON ERROR: ', str(e))
        pass
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


def get_jsondata_from_url_with_tablename(url, tablename):
    data = get_jsondata_from_url(url)
    if data is None:
        return None
    result = {}
    for key, value in data.items():
        result['CL_%s_%s' % (tablename, key)] = value

    return result


def convert_all_keys_with_tablename(data, tablename):
    result = {}
    for key, value in data.items():
        result['CL_%s_%s' % (tablename, key)] = value

    return result
