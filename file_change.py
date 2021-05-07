import glob
import pandas as pd
from docx2pdf import convert
import os
import subprocess
import pathlib

def check_docu():
        files_checked = []
        types = ('*.doc', '*.docx', '*.psd', '*.mov', '*.accdb', '*.xlsx', '*.xls', '*.xlsm', '*.ppt', '*.pptx', '*.wmv', '*.wma', '*.wpl', '*.R', '*.py')
      
        for files in types:
            files_checked.extend(glob.glob(files))
        print(files_checked)

        if len(files_checked) >= 1:
            num_files = len(files_checked)
            print(str(num_files) + ' files to be changed!')
            cont = input("Convert all files? y/n  ")
            if cont == 'y':
                convert_files(files_checked)
            if cont == 'n':
                print('okay')
            elif cont != 'y' and cont != 'n':
                print('Please type y or n.')

        if len(files_checked) == 0:
            print('No files to convert.')

def convert_files(files_checked):
        csv_matchers = ['xls','xlsx']
        csv_matching = [s for s in files_checked if any(xs in s for xs in csv_matchers)]
        if len(csv_matching) >= 1:
            for x in csv_matching:
                data_xls = pd.read_excel(x, index_col=None)
                data_xls.to_csv((x + '.csv'), encoding='utf-8', index=False)

        doc_matchers = ['doc','docx']
        doc_matching = [s for s in files_checked if any(xs in s for xs in doc_matchers)]
        if len(doc_matching) >= 1:
            for x in doc_matching:
                 convert(x, (x + '.pdf'))

        mov_matchers = ['mov']
        mov_matching = [s for s in files_checked if any(xs in s for xs in mov_matchers)]
        if len(mov_matching) >= 1:
            for x in mov_matching:
                 y = str(pathlib.Path(x).parent.absolute())
                 z = (y + '/' + x)
                 a = (y + '/' + 'test.mp4')
                 subprocess.Popen(['ffmpeg', '-i', x, '-vcodec', 'h264', '-acodec', 'aac', (x + '.mp4')])

        sound_matchers = ['wma', 'mp3']
        sound_matching = [s for s in files_checked if any(xs in s for xs in sound_matchers)]
        if len(sound_matching) >= 1:
            for x in sound_matching:
                subprocess.Popen(['ffmpeg', '-i', x, (x + '.wav')])

        ppt_matchers = ['ppt', 'pptx']
        ppt_matching = [s for s in files_checked if any(xs in s for xs in ppt_matchers)]
        if len(ppt_matching) >= 1:
            for x in ppt_matching:
                lib_dir = '/Applications/LibreOffice.app/Contents/MacOS'
                if os.path.exists(lib_dir) and os.path.isdir(lib_dir):
                    os.chdir(lib_dir)
                    subprocess.Popen(['./soffice',  '--headless', '--invisible', '--convert-to', 'pdf', '--outdir', '[YOUR OUT DIRECTORY]', '[LOCATION OF FILE YOU WANT TO CHANGE]'])
            
        
        r_matchers = ['.R']
        r_matching = [s for s in files_checked if any(xs in s for xs in r_matchers)]
        if len(r_matching) >= 1:
                 for r in r_matching:
                     try:
                         print(r)
                         subprocess.check_output(["sudo", "R", "CMD", "check", r])
                     except subprocess.CalledProcessError as e:
                         continue

        py_matchers = ['py']
        py_matching = [s for s in files_checked if any(xs in s for xs in py_matchers)]
        if len(py_matching) >= 1:
                 for p in py_matching:
                     try:
                         print(p)
                         subprocess.check_output(['python3', '-m', 'py_compile', p])
                     except subprocess.CalledProcessError as e:
                         continue
        
check_docu()
