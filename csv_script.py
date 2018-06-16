__author__ = 'Region Star'

import csv

from settings import BaseConfig


def read_titles_from_csv_file(csvfilepath):
    print('---------------------------------------')
    print('Reading CSV File & Making Hash Table ..... Started .....')

    # Get Total records
    # with open(csvfilepath) as csvfile:
    #     readcsv = csv.reader(csvfile, delimiter=',')
    #     total_row_count = sum(1 for tmprow in readcsv)
    total_row_count = 30077056 + 1
    prevpercent = 0
    with open(csvfilepath) as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')
        # citing_opinion_id, cited_opinion_id
        dictcitations = {}
        dictcounts = {}
        cnt = 0
        tmpcitingid = ''
        for row in readcsv:
            if cnt == 0:
                # skip column names
                cnt += 1
                continue

            if tmpcitingid != row[0]:
                tmpcitingid = row[0]
                dictcitations[tmpcitingid] = []
            dictcitations[tmpcitingid].append(row[1])

            if row[1] not in dictcounts:
                dictcounts[row[1]] = 1
            else:
                dictcounts[row[1]] += 1
            cnt += 1

            # Show Percent
            curpercent = 100.0 * cnt / total_row_count
            if curpercent - prevpercent >= 0.1:
                print('%.2f%s : %d/%d' % (curpercent, '%', cnt, total_row_count))
                prevpercent = curpercent

            if BaseConfig.DEBUG and cnt > BaseConfig.CSV_ITEM_LIMIT:
                break
    print('%.2f%s : %d/%d' % (curpercent, '%', cnt, total_row_count))
    print('Reading CSV File & Making Hash Table ..... Completed .....')
    return dictcitations, dictcounts
