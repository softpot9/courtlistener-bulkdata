__author__ = 'Region Star'
import json
import re
from pprint import pprint
from datetime import datetime, date
import urllib
from pymongo import MongoClient
from bson.objectid import ObjectId
import glob

from settings import BaseConfig
from csv_script import read_titles_from_csv_file
from bulkapi import get_jsondata_from_id, get_jsondata_from_url

"""
    MongoDB database connection and close
"""
def mongodb_connection():
    dbuser = BaseConfig.MONGODB_USER
    dbpasswd = urllib.parse.quote(BaseConfig.MONGODB_PWD, safe='')
    # dbpasswd = urllib.quote_plus(BaseConfig.MONGODB_PWD)
    if BaseConfig.IS_LOCAL_DB:
        if dbuser == '':
            client = MongoClient('mongodb://' + BaseConfig.MONGODB_HOSTNAME)
        else:
            client = MongoClient('mongodb://' + dbuser + ':' + dbpasswd + '@' + BaseConfig.MONGODB_HOSTNAME)
        db = client[BaseConfig.MONGODB_DBNAME]
    else:
        tmpsettings = {
            'host': BaseConfig.MONGODB_HOSTNAME,
            'username': dbuser,
            'password': dbpasswd,
            'options': "?authSource=" + BaseConfig.MONGODB_DBNAME + "&replicaSet=6d1193fcb24a46dfa2383d329f86cf6e"
        }
        client = MongoClient("mongodb://{username}:{password}@{host}/{options}".format(**tmpsettings))
        db = client[BaseConfig.MONGODB_DBNAME]

    return client, db


def mongodb_close(client):
    client.close()

gIssueCourts = []
def get_record_data_by_opinion_id(_id, dict_citations, dict_counts):
    record = {
        'Reporter_Citation': '',
                            # From "/Opinion", follow the link in the "cluster" field
                            # within "/Cluster",
                            #
                            # IF "neutral_cite" <> null OR ""
                            # THEN use value at "neutral_cite"
                            # ELSE
                            #
                            # IF "federal_cite_one" <> null OR ""
                            # THEN use value at "federal_cite_one"
                            # ELSE
                            #
                            # IF "federal_cite_two" <> null OR ""
                            # THEN use value at "federal_cite_two"
                            # ELSE
                            #
                            # IF "federal_cite_three" <> null OR ""
                            # THEN use value at "federal_cite_three"
                            # ELSE
                            #
                            # IF "scotus_early_cite" <> null OR ""
                            # THEN use value at "scotus_early_cite"
                            # ELSE
                            #
                            # IF "specialty_cite_one" <> null OR ""
                            # THEN use value at "specialty_cite_one"
                            # ELSE
                            #
                            # IF "state_cite_regional" <> null OR ""
                            # THEN use value at "state_cite_regional"
                            # ELSE
                            #
                            # IF "state_cite_one" <> null OR ""
                            # THEN use value at "state_cite_one"
                            # ELSE print, ""
                            #
                            # IF "state_cite_two" <> null OR ""
                            # THEN use value at "state_cite_two"
                            # ELSE
                            #
                            # IF "state_cite_three" <> null OR ""
                            # THEN use value at "state_cite_three"
                            # ELSE print ""
        'Data_source': 'Court Listener', # fixed value "Court Listener"
        'Court': '',
                    # From "/Opinion", follow the link in the "cluster" field
                    # within "/Cluster", follow the link in the "docket" field
                    # within "/Docket", follow the link in the "court" field
                    # within "/Court", print the value at "full_name"
        'Title': '',
                    # From "/Opinion", follow the link in the "cluster" field
                    # within "/Cluster", print the value at "case_name"
        'TF_IDF_Tags': [], # leave empty
        'Searchtags': [], # leave empty
        'Duplicate': 'No', # fixed value = "No"
        'Text_Level_Notes': [], # leave empty
        'PartyType2': '', # fixed value = ""
        'PartyType1': '', # fixed value = ""
        'ML_Tags_Doc_Level': [], # leave empty
        'old_Case_Citation': '', # fixed value = ""
        'Old_Case_No': '', # fixed value = ""
        'Cases_Cited_Link': [], # within "/Opinion", print the value at "opinions_cited"
        'Text_Level_Tags': [], # leave empty
        'HTML_Stored': 1, # fixed value = NumberInt(1)
        'URL': '', # within "/Opinion", print the value at "download_url"
        'Review_Status': 'Yet To Start', # fixed value = "Yet To Start"
        'Cited_No': 0,
                    # From "/Opinion", grab the value from the field "id"
                    # Go to the "Citations.all.csv" and search for the /Opinion/id in the cited_opinion_id column of the CSV
                    # Print  the count of the number of occurances of that "id" within the cited_opinion_id
        'HTMLtext': '', #IF "html_with_citations" <> null OR ""
                        # THEN use value at "html_with_citations"
                        # ELSE
                        #    IF "html_columbia" <> null OR ""
                        #    THEN use value at "html_columbia"
                        #    ELSE
                        #       IF "html_lawbox" <> null OR ""
                        #       THEN use value at "html_lawbox"
                        #       ELSE
                        #           IF "html" <> null OR ""
                        #           THEN use value at "html"
                        #           ELSE print, ""
                        #           IF "plain_text" <> null OR ""
                        #           THEN use value at "plain_text"
                        #           ELSE
        'Party1': [],
                        # From "/Opinion", follow the link in the "cluster" field
                        # within "/Cluster", follow the link in the "docket" field
                        # within "/Docket", grab the value in the "case_name" field
                        # strip everything after the text "v." including the text "v." itself
                        # (Example)
                        # IF "case_name" = "Fleet v. Entertainment",
                        # THEN the value for "Party1"= "Fleet"
        'Searchterm': [], # leave empty
        'Manual_Tags': [], # leave empty
        'Rule_Tags': '', # fixed value = ""
        'ML_Tags_Text': [], # leave empty
        'Party2': [],
                        # From "/Opinion", follow the link in the "cluster" field
                        # within "/Cluster", follow the link in the "docket" field
                        # within "/Docket", grab the value in the "case_name" field
                        # strip everything before the text "v." - including the text "v." itself
                        # (Example)
                        # IF "case_name" = "Fleet v. Entertainment",
                        # THEN the value for "Party2"= "Entertainment"
        'ML_Tags': [], # leave empty
        'Case_No': '',
                        # "From ""/Opinion"", follow the link in the ""cluster"" field
                        # within ""/Cluster"", follow the link in the ""docket"" field
                        # within ""/Docket"", print the value at ""docket_number"""
        'Cases_Cited': [],
                        # From "/Opinion", grab the value from the field "id"
                        # Go to the "Citations.all.csv" and search for the "/Opinion" "id" in the citing_opinion_id column of the CSV

                        # IF there are results
                        # THEN for each result, grab the value from the corresponding cited_opinion_id column within the CSV
                        # THEN go back to the "/Opinions" API associated with that cited_opinion_id

                        # From "/Opinion", follow the link to the "cluster"
                        # within "/Cluster", print the value at "federal_cite_one"

                        # Repeat this for all the matching opinions in the Citations.all.CSV
        'Case_Text': '', # within "/Opinion", print the value at "plain_text"
        'Document_Level_Notes': '', # fixed value = ""
        'Case_ID': '',
                        # From "/Opinion", follow the link in the "cluster" field
                        #
                        # IF within "/Cluster", the value at "federal_cite_one" <> "" OR null
                        # THEN print the value at "federal_cite_one" + value at "date_filed" (date formatted as : 'MONTH DD,YYYY')
                        # ELSE
                        # print the value at /Docket/case_name + value at /Cluster/date_filed (date formatted as : 'MONTH DD,YYYY')
        'Opinion_Date': '',
                        # From "/Opinion", follow the link in the "cluster" field
                        # within "/Cluster", grab the value at "date_filed" and print in ISODate("") format
        'Year': 0,
                        # From "/Opinion", follow the link in the "cluster" field
                        # within "/Cluster", grab the value at "date_filed"
                        # and strip the first 4 characters
                        # and print in NumberInt() format
        'Document_Level_Tags': [],
                        # There will be two objects within each document's "Document_Level_Tags" array (bolded below).
                        #
                        # "ScrapeSource_CL",
                        # "ScrapeDate_MMDDYYYY"
                        #
                        # (where MMDDYYYY is a timestamp of when the script was run)
        'LDA_Model_Tags': [], # leave empty
    }

    opinion = get_jsondata_from_id('opinions', _id)
    if opinion is None: return None
    # if opinion['author']: print(_id, opinion['author'])
    # if len(opinion['joined_by']) > 0:
    #     print(_id, opinion['joined_by'])
    cluster = get_jsondata_from_url(opinion['cluster'])
    if cluster is None: return None

    if cluster['neutral_cite'] is not None and cluster['neutral_cite'] != "":
        record['Reporter_Citation'] = cluster['neutral_cite']
    elif cluster['federal_cite_one'] is not None and cluster['federal_cite_one'] != "":
        record['Reporter_Citation'] = cluster['federal_cite_one']
    elif cluster['federal_cite_two'] is not None and cluster['federal_cite_two'] != "":
        record['Reporter_Citation'] = cluster['federal_cite_two']
    elif cluster['federal_cite_three'] is not None and cluster['federal_cite_three'] != "":
        record['Reporter_Citation'] = cluster['federal_cite_three']
    elif cluster['scotus_early_cite'] is not None and cluster['scotus_early_cite'] != "":
        record['Reporter_Citation'] = cluster['scotus_early_cite']
    elif cluster['specialty_cite_one'] is not None and cluster['specialty_cite_one'] != "":
        record['Reporter_Citation'] = cluster['specialty_cite_one']
    elif cluster['state_cite_regional'] is not None and cluster['state_cite_regional'] != "":
        record['Reporter_Citation'] = cluster['state_cite_regional']
    elif cluster['state_cite_one'] is not None and cluster['state_cite_one'] != "":
        record['Reporter_Citation'] = cluster['state_cite_one']
    elif cluster['state_cite_two'] is not None and cluster['state_cite_two'] != "":
        record['Reporter_Citation'] = cluster['state_cite_two']
    elif cluster['state_cite_three'] is not None and cluster['state_cite_three'] != "":
        record['Reporter_Citation'] = cluster['state_cite_three']
    else:
        record['Reporter_Citation'] = ''

    docket = get_jsondata_from_url(cluster['docket'])
    if docket is None: return None
    court = get_jsondata_from_url(docket['court'])
    if court is None:
        # print(_id, 'Error - Not found courts json file.', docket['court'])
        if docket['court'] not in gIssueCourts:
            gIssueCourts.append(docket['court'])
        record['Court'] = ''
    else:
        record['Court'] = court['full_name']

    record['Title'] = cluster['case_name']

    record['Cases_Cited_Link'] = opinion['opinions_cited']

    record['URL'] = opinion['download_url']

    idopinion = _id #str(opinion['id'])
    if idopinion in dict_counts:
        record['Cited_No'] = dict_counts[str(idopinion)]
    else:
        record['Cited_No'] = 0
        # print('Getting Cited_No Error - Not found cited_opinion_id in CSV file: ', idopinion)

    if opinion['html_with_citations'] is not None and opinion['html_with_citations'] != "":
        record['HTMLtext'] = opinion['html_with_citations']
    elif opinion['html_columbia'] is not None and opinion['html_columbia'] != "":
        record['HTMLtext'] = opinion['html_columbia']
    elif opinion['html_lawbox'] is not None and opinion['html_lawbox'] != "":
        record['HTMLtext'] = opinion['html_lawbox']
    elif opinion['html'] is not None and opinion['html'] != "":
        record['HTMLtext'] = opinion['html']
    elif opinion['plain_text'] is not None and opinion['plain_text'] != "":
        record['HTMLtext'] = opinion['plain_text']
    else:
        record['HTMLtext'] = ''

    record['Party1'] = cluster['case_name'].split("v.", 1)[0].rstrip()

    try:
        record['Party2'] = cluster['case_name'].split("v.", 1)[1].lstrip()
    except Exception as e:
        record['Party2'] = ''
        # print('Getting Party2 Error - not found "v." Invalid Format: ', docket['case_name'])
        # print(str(e))

    if docket['docket_number'] is None or docket['docket_number'] == '':
        record['Case_No'] = ''
    else:
        record['Case_No'] = '-'.join(re.findall(r'\d+', docket['docket_number']))

    record['Cases_Cited'] = []
    if idopinion in dict_citations:
        for cited_opinion_id in dict_citations[idopinion]:
            tmpopinion = get_jsondata_from_id('opinions', cited_opinion_id)
            if tmpopinion is None: return None
            tmpcluster = get_jsondata_from_url(tmpopinion['cluster'])
            if tmpcluster is None: return None
            record['Cases_Cited'].append(tmpcluster['federal_cite_one'])

    record['Case_Text'] = opinion['plain_text']

    try:
        datetime_object = datetime.strptime(cluster['date_filed'], '%Y-%m-%d')
        tmpdatefiled = datetime_object.strftime('%B %d,%Y')
    except Exception as e:
        print('Error - Invalid Date Format. should be %Y-%m-%d. ex:1990-09-23: ', cluster['date_filed'])
        print(str(e))
        tmpdatefiled = ''
        datetime_object = None

    if cluster['federal_cite_one'] is not None and cluster['federal_cite_one'] != '':
        record['Case_ID'] = '%s (%s)' % (cluster['federal_cite_one'], tmpdatefiled)
    else:
        record['Case_ID'] = '%s (%s)' % (docket['case_name'], tmpdatefiled)

    if datetime_object is not None:
        record['Opinion_Date'] = datetime(datetime_object.year, datetime_object.month, datetime_object.day, 0, 0, 0, 0)
    else:
        record['Opinion_Date'] = None

    if datetime_object is not None:
        record['Year'] = datetime_object.year
    else:
        record['Year'] = 0

    record['Document_Level_Tags'] = ['ScrapeSource_CL', 'ScrapeDate_%s' % (datetime.now().strftime('%m%d%Y'))]

    # # for only testing
    # record['Case_Text'] = ''
    # record['HTMLtext'] = ''

    # Additional Fields - Opinion
    record['CL_opinion_id'] = _id
    record['CL_opinion_author_str'] = opinion['author_str']
    record['CL_opinion_date_created'] = opinion['date_created']
    record['CL_opinion_date_modified'] = opinion['date_modified']
    record['CL_opinion_download_url'] = opinion['download_url']
    record['CL_opinion_extracted_by_ocr'] = opinion['extracted_by_ocr']
    record['CL_opinion_local_path'] = opinion['local_path']
    record['CL_opinion_page_count'] = opinion['page_count']
    record['CL_opinion_per_curiam'] = opinion['per_curiam']
    record['CL_opinion_sha1'] = opinion['sha1']
    record['CL_opinion_type'] = opinion['type']
    record['CL_opinion_absolute_url'] = '' if 'absolute_url' not in opinion else opinion['absolute_url']
    record['CL_opinion_resource_uri'] = '' if 'resource_uri' not in opinion else opinion['resource_uri']

    # Additional Fields - Docket
    docket['court'] = court
    docket['assigned_to'] = None if docket['assigned_to'] is None or docket['assigned_to'] == '' else get_jsondata_from_url(docket['assigned_to'])
    docket['referred_to'] = None if docket['referred_to'] is None or docket['referred_to'] == '' else get_jsondata_from_url(docket['referred_to'])

    # Additional Fields - Cluster
    tmp = cluster['panel']
    cluster['panel'] = []
    for v in tmp:
        cluster['panel'].append(None if v is None or v == '' else get_jsondata_from_url(v))

    tmp = cluster['non_participating_judges']
    cluster['non_participating_judges'] = []
    for v in tmp:
        cluster['non_participating_judges'].append(None if v is None or v == '' else get_jsondata_from_url(v))

    cluster['docket'] = docket
    record['CL_opinion_cluster'] = cluster

    record['CL_opinion_author'] = None if opinion['author'] is None or opinion['author'] == '' else get_jsondata_from_url(opinion['author'])

    record['CL_opinion_joined_by'] = []
    for v in opinion['joined_by']:
        record['CL_opinion_joined_by'].append(None if v is None or v == '' else get_jsondata_from_url(v))

    return record


def main():
    dict_citations, dict_counts = read_titles_from_csv_file(BaseConfig.CITATIONS_CSV_FILEPATH)
<<<<<<< HEAD
    # newrecord = get_record_data_by_opinion_id("197526", dict_citations, dict_counts)
    # pprint(newrecord)
=======
    #newrecord = get_record_data_by_opinion_id("4239867", dict_citations, dict_counts)
    #pprint(newrecord)
>>>>>>> d7e8fc630eec8d985bd30faf21f1408aabce107a
    mongoclient, db = mongodb_connection()

    all_opinions_json_files = glob.glob1('bulk-data/opinions', '*.json')
    total_opinions = len(all_opinions_json_files)

    # 4115314 total counts
    print('---------------------------------------')
    print('Processing Bulk Opinions data..... Started .....')
    cnt = 0
    prevpercent = 0
    curpercent = 0
    for v in all_opinions_json_files:
        _id = v.split('.')[0]
        newrecord = get_record_data_by_opinion_id(_id, dict_citations, dict_counts)
        if newrecord is None:
            print('Error - Not found json file. skip it', _id)
            # break
        else:
<<<<<<< HEAD
            if BaseConfig.DEBUG:
                with open('result/%s.json' % _id, 'w') as fp:
                    json.dump(newrecord, fp)
            else:
                db[BaseConfig.MONGODB_COLLECTION].insert(newrecord)
=======
            # db[BaseConfig.MONGODB_COLLECTION].insert(newrecord)
            pass
>>>>>>> d7e8fc630eec8d985bd30faf21f1408aabce107a

        cnt += 1
        # Show Percent
        curpercent = 100.0 * cnt / total_opinions
        if curpercent - prevpercent >= 0.01:
            print('%.2f%s : %d/%d' % (curpercent, '%', cnt, total_opinions))
            prevpercent = curpercent
        if BaseConfig.DEBUG and cnt > BaseConfig.OPINION_LIMIT:
            break
    print('%.2f%s : %d/%d' % (curpercent, '%', cnt, total_opinions))
    print('Processing Bulk Opinions data..... Completed .....')
    print('----- ISSUE COURTS -----')
    pprint(gIssueCourts)
    mongodb_close(mongoclient)

if __name__ == "__main__":
    # tduration = datetime.datetime.utcnow()
    main()
    # print('duration:', datetime.datetime.utcnow() - tduration)
