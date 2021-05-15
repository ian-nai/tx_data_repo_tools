import requests
import json
import xml

base = 'https://dataverse.tdl.org'
rows = 10
start = 0
page = 1
condition = True # emulate do-while


# API: 7fa85ece-2728-459f-abc6-d1b9428e6127
'''
while (condition):

    url = base + '/api/search?q=tree' + "&start=" + str(start)
    resp = requests.get(url, headers={"X-Dataverse-key":"7fa85ece-2728-459f-abc6-d1b9428e6127"})
    data = resp.json()
    total = data['data']['total_count']
    print("=== Page", page, "===")
    print("start:", start, " total:", total)
    for i in data['data']['items']:
        print("- ", i['name'], "(" + i['type'] + ")")
    start = start + rows
    page += 1
    condition = start < total
'''


while (condition):

    file_names = []

    #url = base + '/api/search?q=tree' + "&start=" + str(start)
    url = 'https://dataverse.tdl.org/api/search?q=*&per_page=1000&sort=date&order=asc&q=*&fq=dateSort:[2021-05-01T00:00:00Z+TO+2021-05-09T00:00:00Z]'

    resp = requests.get(url, headers={"X-Dataverse-key":"7fa85ece-2728-459f-abc6-d1b9428e6127"})
    data = resp.json()
    total = data['data']['total_count']
    print("=== Page", page, "===")
    print("start:", start, " total:", total)
    for i in data['data']['items']:
        print("- ", i['name'], "(" + i['type'] + ")")
        file_names.append(i['name'] + " (" + i['type'] + ") ")
    start = start + rows
    page += 1
    condition = start < total



    smallerlist = [l.split(',') for l in ','.join(file_names).split('(dataset)')]
    print(smallerlist)

dataset_list = []

# for x in file_names:
#     if '(dataset)' in x:
#         dataset_list.append(x)

for y in smallerlist:
    for x in y:
        if '(file)' not in x:
            y.remove(x)
            dataset_list.append(x)

dataset_list2 = [x for x in dataset_list if x != []]
smallerlist2 = [x for x in smallerlist if x != []]

dataset_list3 = []
for item in dataset_list2:
    if item != ' ':
        dataset_list3.append(str(item))


print(dataset_list3)


final_list = []
q = len(smallerlist)

count = 0
for x in smallerlist2:
    x.insert(0,dataset_list3[count])
    count += 1

# smallerlist3 = []
# for lists in smallerlist2:
#     for item in lists:
#         if item:
#             smallerlist3.append(item)

print(smallerlist2)

import xlsxwriter

workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A', 14)

#cell_format = workbook.add_format()
format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

for row, row_data in enumerate(smallerlist2):
    worksheet.write_row(row + 1, 1, row_data)

worksheet.conditional_format('A2:K7', {'type': 'text',
                                       'criteria': 'ends with',
                                       'value': '.zipC (file) ',
                                       'format': format1})

worksheet.conditional_format('A2:K7', {'type': 'text',
                                       'criteria': 'ends with',
                                       'value': '.pdf (file) ',
                                       'format': format1})
#pdf (file)
workbook.close()


import csv

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(smallerlist2)



# https://guides.dataverse.org/en/latest/api/search.html#

# basically: search for dataverses
# iterate through dataverses to get file types
# from there, determine number of file infractions
# could do only dataverses within certain time frame, etc.
