import requests
import json
import xml

base = 'https://dataverse.tdl.org'
rows = 10
start = 0
page = 1
condition = True 


while (condition):

    file_names = []
    url = 'https://dataverse.tdl.org/api/search?q=*&per_page=1000&sort=date&order=asc&q=*&fq=dateSort:[2021-05-01T00:00:00Z+TO+2021-05-09T00:00:00Z]'
    resp = requests.get(url, headers={"X-Dataverse-key":"[YOUR KEY]"})
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



    split_list = [l.split(',') for l in ','.join(file_names).split('(dataset)')]

dataset_list = []
for y in split_list:
    for x in y:
        if '(file)' not in x:
            y.remove(x)
            dataset_list.append(x)

dataset_list_cleaned = [x for x in dataset_list if x != []]
final_list = [x for x in split_list if x != []]

dataset_list_final = []
for item in dataset_list_cleaned:
    if item != ' ':
        dataset_list_final.append(str(item))

count = 0
for x in final_list:
    x.insert(0,dataset_list_final[count])
    count += 1

print(final_list)

import xlsxwriter

workbook = xlsxwriter.Workbook('dataverse_search.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A', 14)

format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

for row, row_data in enumerate(final_list):
    worksheet.write_row(row + 1, 1, row_data)

worksheet.conditional_format('A2:K7', {'type': 'text',
                                       'criteria': 'ends with',
                                       'value': '.zipC (file) ',
                                       'format': format1})

worksheet.conditional_format('A2:K7', {'type': 'text',
                                       'criteria': 'ends with',
                                       'value': '.pdf (file) ',
                                       'format': format1})

workbook.close()


import csv

with open("dataverse_search.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_list)
