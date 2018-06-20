__author__ = 'Region Star'
import json
from pprint import pprint
from datetime import datetime

from settings import BaseConfig
from csv_script import read_titles_from_csv_file

import re

s = None
print('-'.join(re.findall(r'\d+', s)))


# def get_jsondata_from_id(stype, id):
#     filepath = 'bulk-data/%s/%s.json' % (stype, str(id))
#     try:
#         with open(filepath) as f:
#             data = json.load(f)
#         return data
#     except Exception as e:
#         print('Load JSON ERROR: ', str(e))
#     return None
#
#
# def get_jsondata_from_url(url):
#     tmparr = url.split('/')
#     tmpid = tmparr[-1]
#     if tmpid == '':
#         tmpid = tmparr[-2]
#         tmptype = tmparr[-3]
#     else:
#         tmptype = tmparr[-2]
#
#     return get_jsondata_from_id(tmptype, tmpid)
#
# dict_citations, dict_counts = read_titles_from_csv_file(BaseConfig.csvfilename)
#
# record = {
#     'Reporter_Citation': '',
#                             # From "/Opinion", follow the link in the "cluster" field
#                             # within "/Cluster", print the value at "federal_cite_one"
#     'Data_source': 'Court Listener', # fixed value "Court Listener"
#     'Court': '',
#                 # From "/Opinion", follow the link in the "cluster" field
#                 # within "/Cluster", follow the link in the "docket" field
#                 # within "/Docket", follow the link in the "court" field
#                 # within "/Court", print the value at "full_name"
#     'Title': '',
#                 # From "/Opinion", follow the link in the "cluster" field
#                 # within "/Cluster", follow the link in the "docket" field
#                 # within "/Docket", print the value at "case_name"
#     'TF_IDF_Tags': [], # leave empty
#     'Searchtags': [], # leave empty
#     'Duplicate': 'No', # fixed value = "No"
#     'Text_Level_Notes': [], # leave empty
#     'PartyType2': '', # fixed value = ""
#     'PartyType1': '', # fixed value = ""
#     'ML_Tags_Doc_Level': [], # leave empty
#     'old_Case_Citation': '', # fixed value = ""
#     'Old_Case_No': '', # fixed value = ""
#     'Cases_Cited_Link': [], # within "/Opinion", print the value at "opinions_cited"
#     'Text_Level_Tags': [], # leave empty
#     'HTML_Stored': 1, # fixed value = NumberInt(1)
#     'URL': '', # within "/Opinion", print the value at "download_url"
#     'Review_Status': 'Yet To Start', # fixed value = "Yet To Start"
#     'Cited_No': 0,
#                 # From "/Opinion", grab the value from the field "id"
#                 # Go to the "Citations.all.csv" and search for the /Opinion/id in the cited_opinion_id column of the CSV
#                 # Print  the count of the number of occurances of that "id" within the cited_opinion_id
#     'HTMLtext': '', #IF "html_with_citations" <> null OR ""
#                     # THEN use value at "html_with_citations"
#                     # ELSE
#                     #    IF "html_columbia" <> null OR ""
#                     #    THEN use value at "html_columbia"
#                     #    ELSE
#                     #       IF "html_lawbox" <> null OR ""
#                     #       THEN use value at "html_lawbox"
#                     #       ELSE
#                     #           IF "html" <> null OR ""
#                     #           THEN use value at "html"
#                     #           ELSE print, ""
#                     #           IF "plain_text" <> null OR ""
#                     #           THEN use value at "plain_text"
#                     #           ELSE
#     'Party1': [],
#                     # From "/Opinion", follow the link in the "cluster" field
#                     # within "/Cluster", follow the link in the "docket" field
#                     # within "/Docket", grab the value in the "case_name" field
#                     # strip everything after the text "v." including the text "v." itself
#                     # (Example)
#                     # IF "case_name" = "Fleet v. Entertainment",
#                     # THEN the value for "Party1"= "Fleet"
#     'Searchterm': [], # leave empty
#     'Manual_Tags': [], # leave empty
#     'Rule_Tags': '', # fixed value = ""
#     'ML_Tags_Text': [], # leave empty
#     'Party2': [],
#                     # From "/Opinion", follow the link in the "cluster" field
#                     # within "/Cluster", follow the link in the "docket" field
#                     # within "/Docket", grab the value in the "case_name" field
#                     # strip everything before the text "v." - including the text "v." itself
#                     # (Example)
#                     # IF "case_name" = "Fleet v. Entertainment",
#                     # THEN the value for "Party2"= "Entertainment"
#     'ML_Tags': [], # leave empty
#     'Case_No': '',
#                     # "From ""/Opinion"", follow the link in the ""cluster"" field
#                     # within ""/Cluster"", follow the link in the ""docket"" field
#                     # within ""/Docket"", print the value at ""docket_number"""
#     'Cases_Cited': [],
#                     # From "/Opinion", grab the value from the field "id"
#                     # Go to the "Citations.all.csv" and search for the "/Opinion" "id" in the citing_opinion_id column of the CSV
#
#                     # IF there are results
#                     # THEN for each result, grab the value from the corresponding cited_opinion_id column within the CSV
#                     # THEN go back to the "/Opinions" API associated with that cited_opinion_id
#
#                     # From "/Opinion", follow the link to the "cluster"
#                     # within "/Cluster", print the value at "federal_cite_one"
#
#                     # Repeat this for all the matching opinions in the Citations.all.CSV
#     'Case_Text': '', # within "/Opinion", print the value at "plain_text"
#     'Document_Level_Notes': '', # fixed value = ""
#     'Case_ID': '',
#                     # From "/Opinion", follow the link in the "cluster" field
#                     #
#                     # IF within "/Cluster", the value at "federal_cite_one" <> "" OR null
#                     # THEN print the value at "federal_cite_one" + value at "date_filed" (date formatted as : 'MONTH DD,YYYY')
#                     # ELSE
#                     # print the value at /Docket/case_name + value at /Cluster/date_filed (date formatted as : 'MONTH DD,YYYY')
#     'Opinion_Date': '',
#                     # From "/Opinion", follow the link in the "cluster" field
#                     # within "/Cluster", grab the value at "date_filed" and print in ISODate("") format
#     'Year': 0,
#                     # From "/Opinion", follow the link in the "cluster" field
#                     # within "/Cluster", grab the value at "date_filed"
#                     # and strip the first 4 characters
#                     # and print in NumberInt() format
#     'Document_Level_Tags': [],
#                     # There will be two objects within each document's "Document_Level_Tags" array (bolded below).
#                     #
#                     # "ScrapeSource_CL",
#                     # "ScrapeDate_MMDDYYYY"
#                     #
#                     # (where MMDDYYYY is a timestamp of when the script was run)
#     'LDA_Model_Tags': [], # leave empty
# }
#
# print('--------------- Start ---------------')
# opinion = get_jsondata_from_id('opinions', 197526)
# cluster = get_jsondata_from_url(opinion['cluster'])
# record['Reporter_Citation'] = cluster['federal_cite_one']
#
# docket = get_jsondata_from_url(cluster['docket'])
# court = get_jsondata_from_url(docket['court'])
# record['Court'] = court['full_name']
#
# record['Title'] = docket['case_name']
#
# record['Cases_Cited_Link'] = opinion['opinions_cited']
#
# record['URL'] = opinion['download_url']
#
# idopinion = str(opinion['id'])
# if idopinion in dict_counts:
#     record['Cited_No'] = dict_counts[str(idopinion)]
# else:
#     record['Cited_No'] = 0
#     print('Getting Cited_No Error - Not found cited_opinion_id in CSV file: ', idopinion)
#
# if opinion['html_with_citations'] is not None and opinion['html_with_citations'] != "":
#     record['HTMLtext'] = opinion['html_with_citations']
# elif opinion['html_columbia'] is not None and opinion['html_columbia'] != "":
#     record['HTMLtext'] = opinion['html_columbia']
# elif opinion['html_lawbox'] is not None and opinion['html_lawbox'] != "":
#     record['HTMLtext'] = opinion['html_lawbox']
# elif opinion['html'] is not None and opinion['html'] != "":
#     record['HTMLtext'] = opinion['html']
# else:
#     record['HTMLtext'] = opinion['plain_text']
#
# record['Party1'] = docket['case_name'].split("v.", 1)[0].rstrip()
#
# try:
#     record['Party2'] = docket['case_name'].split("v.", 1)[1].lstrip()
# except Exception, e:
#     record['Party2'] = ''
#     print('Getting Party2 Error - not found "v." Invalid Format: ', docket['case_name'])
#     print(str(e))
#
# record['Case_No'] = docket['docket_number']
#
# record['Cases_Cited'] = []
# if idopinion in dict_citations:
#     for cited_opinion_id in dict_citations[idopinion]:
#         tmpopinion = get_jsondata_from_id('opinions', cited_opinion_id)
#         tmpcluster = get_jsondata_from_url(tmpopinion['cluster'])
#         record['Cases_Cited'].append(tmpcluster['federal_cite_one'])
#
# record['Case_Text'] = opinion['plain_text']
#
# try:
#     datetime_object = datetime.strptime(cluster['date_filed'], '%Y-%m-%d')
#     tmpdatefiled = datetime_object.strftime('%B %d,%Y')
# except Exception, e:
#     print('Error - Invalid Date Format. should be %Y-%m-%d. ex:19990-09-23: ', cluster['date_filed'])
#     print(str(e))
#     tmpdatefiled = ''
#     datetime_object = None
#
# if cluster['federal_cite_one'] is not None and cluster['federal_cite_one'] != '':
#     record['Case_ID'] = '%s (%s)' % (cluster['federal_cite_one'], tmpdatefiled)
# else:
#     record['Case_ID'] = '%s (%s)' % (docket['case_name'], tmpdatefiled)
#
# if datetime_object is not None:
#     record['Opinion_Date'] = datetime_object.isoformat()
# else:
#     record['Opinion_Date'] = None
#
# if datetime_object is not None:
#     record['Year'] = datetime_object.year
# else:
#     record['Year'] = 0
#
# record['Document_Level_Tags'] = ['ScrapeSource_CL', 'ScrapeDate_%s' % (datetime.now().strftime('%m%d%Y'))]
#
#
