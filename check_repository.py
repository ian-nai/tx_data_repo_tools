import requests
import json
import xml
import os.path
import glob
import pandas as pd
from docx2pdf import convert
import os
import subprocess
import shutil
from send2trash import send2trash

class TX:
    dataverse_server = 'https://demo.dataverse.org' # no trailing slash
    api_key = '[YOUR KEY]'
    dataset_id = 1234567  # database id of the dataset
    persistentId = 'doi:12.34567/ABC/123456' # doi or hdl of the dataset

    prop_file_ids = []
    files_to_upload = []
    files_checked = []

    types = ['.doc', '.docx', '.psd', '.mov', '.accdb', '.xlsx', '.xls', '.xlsm', '.ppt', '.pptx', '.wmv', '.wma', '.mp3', '.wpl']

    def check_dataset(doi):
        url = (TX.dataverse_server + '/api/datasets/:persistentId/?persistentId=doi:' + doi)
        resp = requests.get(url)
        data = resp.json()
        dataset_id = (data['data']['latestVersion']['datasetId'])
        version_number = (data['data']['latestVersion']['versionNumber'])

        TX.get_files(dataset_id, version_number)

    def get_files(id, version_number):
        url = TX.dataverse_server + str(id) + '/versions/' + str(version_number) + '/files'

        resp = requests.get(url)
        data = resp.json()

        list_of_file_ids = []
        list_of_filenames = []
        list_of_contentTypes = []

        for x in data['data']:
            list_of_file_ids.append(x['dataFile']['id'])
            list_of_filenames.append(x['dataFile']['filename'])
            list_of_contentTypes.append(x['dataFile']['contentType'])

        id_filename_list = tuple(zip(list_of_file_ids, list_of_filenames))

        print(id_filename_list)

        proprietary_formats = []

        for id in id_filename_list:
            for type in TX.types:
                if type in str(id):
                    print(id)
                    proprietary_formats.append(id)

        TX.prop_file_ids.append(proprietary_formats)
        print(TX.prop_file_ids)


    def check_directory(directory):
         types = ['**/*.doc', '**/*.docx', '**/*.psd', '**/*.mov', '**/*.accdb', '**/*.xlsx', '**/*.xls', '**/*.xlsm', '**/*.ppt', '**/*.pptx', '**/*.wmv', '**/*.wma', '**/*.mp3', '**/*.wpl']

         for type in types:
            for file in glob.glob(type, recursive=True):
                print(file)
                TX.files_checked.append(file)

         TX.files_checked = [file for file in files_checked if not file.startswith('venv')]

         print(TX.files_checked)

         if len(TX.files_checked) >= 1:
            num_files = len(files_checked)
            print(str(num_files) + ' files to be changed!')
            cont = input("Convert all files? y/n  ")
            if cont == 'y':
                convert_files(files_checked)
            if cont == 'n':
                print('okay')
            elif cont != 'y' and cont != 'n':
                print('Please type y or n.')

         if len(TX.files_checked) == 0:
            print('No files to convert.')

    def convert_files():
        cur_full_path = os.path.abspath(os.getcwd())

        csv_matchers = ['xls','xlsx']
        csv_matching = [s for s in TX.files_checked if any(xs in s for xs in csv_matchers)]
        if len(csv_matching) >= 1:
            for x in csv_matching:
                data_xls = pd.read_excel(x, index_col=None)
                data_xls.to_csv((x + '.csv'), encoding='utf-8', index=False)


        doc_matchers = ['doc','docx']
        doc_matching = [s for s in TX.files_checked if any(xs in s for xs in doc_matchers)]
        if len(doc_matching) >= 1:
            for x in doc_matching:
                 convert(x, (x + '.pdf'))

        mov_matchers = ['mov']
        mov_matching = [s for s in TX.files_checked if any(xs in s for xs in mov_matchers)]
        if len(mov_matching) >= 1:
            for x in mov_matching:
                 subprocess.Popen(['ffmpeg', '-i', x, '-vcodec', 'h264', '-acodec', 'aac', (x + '.mp4')])

        sound_matchers = ['wma', 'mp3']
        sound_matching = [s for s in TX.files_checked if any(xs in s for xs in sound_matchers)]
        if len(sound_matching) >= 1:
            for x in sound_matching:
                subprocess.Popen(['ffmpeg', '-i', x, (x + '.wav')])

        ppt_matchers = ['ppt', 'pptx']
        ppt_matching = [s for s in TX.files_checked if any(xs in s for xs in ppt_matchers)]
        if len(ppt_matching) >= 1:
            for x in ppt_matching:
                lib_dir = '/Applications/LibreOffice.app/Contents/MacOS'
                if os.path.exists(lib_dir) and os.path.isdir(lib_dir):
                    os.chdir(lib_dir)
                    subprocess.Popen(['./soffice',  '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', cur_full_path, cur_full_path])

        for file in TX.files_checked:
            no_extension = file.split(".")[-1]
            TX.files_to_upload.append(no_extension)


    def local_delete():
        cur_full_path = os.path.abspath(os.getcwd())

        for file in TX.files_checked:
            if not file.endswith('.py') and not file.endswith('.R'):
                send2trash(file)


    def delete_and_upload_to_repo():
        for file in TX.files_checked:
            file_exists = os.path.exists(file)
            if file_exists:
                  # delete
                  fileId = TX.prop_file_ids[index_num]


                  url_dataset_id = '%s/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/%s' % (TX.dataverse_server, fileId)

                  print('-' * 40)
                  print('making request: %s' % url_dataset_id)
                  r = requests.delete(url_dataset_id, auth=('$API_TOKEN', TX.api_key))

                  print('-' * 40)
                  print(r.status_code)

              index_num += 1

          files = [f for f in os.listdir('.') if os.path.isfile(f)]
          for f in files:
              if f.split(".")[-1] in TX.files_to_upload:
                  if f.split(".")[0] not in TX.types:
                      # upload
                      file_content = 'content: %s' % datetime.now()
                      files = {'file': (f, file_content)}

                      params = dict(description='Non-proprietary format.')

                      params_as_json_string = json.dumps(params)

                      payload = dict(jsonData=params_as_json_string)


                      url_dataset_id = '%s/api/datasets/%s/add?key=%s' % (TX.dataverse_server, TX.dataset_id, TX.api_key)


                      print('-' * 40)
                      print('making request: %s' % url_dataset_id)
                      r = requests.post(url_dataset_id, data=payload, files=files)

                      print('-' * 40)
                      print(r.json())
                      print(r.status_code)
                  else:
                      continue
               else:
                   continue

       def delete_from_repo():

           for file in TX.files_checked:
               file_exists = os.path.exists(file)
               index_num = 0
               if file_exists:
                   # delete
                   fileId = TX.prop_file_ids[index_num]


                   url_dataset_id = '%s/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/%s' % (TX.dataverse_server, fileId)

                   print('-' * 40)
                   print('making request: %s' % url_dataset_id)
                   r = requests.delete(url_dataset_id, auth=('$API_TOKEN', TX.api_key))

                   print('-' * 40)
                   print(r.status_code)

               index_num += 1

       def upload_to_repo():
             files = [f for f in os.listdir('.') if os.path.isfile(f)]
             for f in files:
                 if f.split(".")[-1] in TX.files_to_upload:
                     if f.split(".")[0] not in TX.types:
                         # upload
                         file_content = 'content: %s' % datetime.now()
                         files = {'file': (f, file_content)}

                         params = dict(description='Non-proprietary format.')

                         params_as_json_string = json.dumps(params)

                         payload = dict(jsonData=params_as_json_string)


                         url_dataset_id = '%s/api/datasets/%s/add?key=%s' % (TX.dataverse_server, TX.dataset_id, TX.api_key)


                         print('-' * 40)
                         print('making request: %s' % url_dataset_id)
                         r = requests.post(url_dataset_id, data=payload, files=files)

                         print('-' * 40)
                         print(r.json())
                         print(r.status_code)
                     else:
                         continue
                  else:
                      continue
