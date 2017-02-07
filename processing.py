import os
import numpy as np
import datetime
from stretchscript import *

print('Welcome to YeastYogi...')
print('Initializing...')

pwd = os.getcwd()
YOGI_PATH = os.path.join(pwd,'YeastYogi')
if not os.path.isdir(YOGI_PATH):
    os.mkdir(YOGI_PATH)
BASE_PATH = os.path.join(pwd,'chromoshake_centromere')
PSF_FILE = os.path.join(BASE_PATH,'GFPbigain.txt')

if not os.path.exists(PSF_FILE):
    raise Exception('Please check there is a PSF file in '+BASE_PATH)


out_files = ['WT.out','no_coh.out','no_cond.out','no_coh_no_cond.out']

#Need the number of beads for each file
number_dict = {
'WT.out':,
'no_coh.out':,
'no_cond.out':,
'no_coh_no_cond.out'
}

#convert the excel files
EXCEL_PATH = os.path.join(BASE_PATH, '5000trimmed_MSD_analysis',)
COH_PATH = os.path.join(EXCEL_PATH,'6p8_coh_SRC')
NO_COH_PATH = os.path.join(EXCEL_PATH,'6p8_no_coh_SRC')

print('Converting color files...')
COH_PATH_OUT = os.path.join(YOGI_PATH,'6p8_coh_SRC')
NO_COH_PATH_OUT = os.path.join(YOGI_PATH,'6p8_no_coh_SRC')
if not os.path.isidr(COH_PATH_OUT):
    os.mkdir(COH_PATH_OUT)
    convertColorFiles(COH_PATH,COH_PATH_OUT,number_dict['WT.out'])
if not os.path.isidr(NO_COH_PATH_OUT):
    os.mkdir(NO_COH_PATH_OUT)
    convertColorFiles(NO_COH_PATH,NO_COH_PATH_OUT,number_dict['no_coh.out'])



#convert the outfiles -- take off header and multiply
for f in out_files:
    path = os.path.join(BASE_PATH,f)
    processHeaderMicrons(path,YOGI_PATH,number_dict[f])

#for each SRC, output a shorter text file
#parseBrownian
#BrownianXMLtoTIFF
print('Processing files...')
temp_file = os.path.join(YOGI_PATH,'temp.txt')
for f in out_files:
    condition = f.split(.)[0]
    condition_path = os.path.join(YOGI_PATH,condition)
    file_path = os.path.join(YOGI_PATH,condition+'.txt')
    coh_path = os.path.join(condition_path,'coh')
    no_coh_path = os.path.join(condition_path,'no_coh')
    if not os.path.isdir(condition_path):
        os.mkdir(condition_path)
    if not os.path.isdir(coh_path):
        os.mkdir(coh_path)
    if not os.path.isdir(no_coh_path):
        os.mkdir(no_coh_path)
    for SRC in os.listdir(COH_PATH_OUT):
        out_path = os.path.join(coh_path,SRC.split('.')[0])
        SRC_path = os.path.join(COH_PATH_OUT,SRC)
        tiff_path = os.path.join(coh_path,SRC.split('.')[0]+'_tiff')

        if not os.path.isdir(out_path):
            os.mkdir(out_path)
            print(out_path)
            os.system("python ParseBrownian.py -PSF {} -out {} -width 75 -height 75 -every 25 {} {}".format(PSF_FILE,out_path,SRC_path,file_path))
        if not os.path.isdir(tiff_path):
            os.mkdir(tiff_path)
            os.system("python BrownianXMLtoTIFF.py -green -out {} {}".format(tiff_path,out_path))
    for SRC in os.listdir(NO_COH_PATH_OUT):
        out_path = os.path.join(no_coh_path,SRC.split('.')[0])
        SRC_path = os.path.join(NO_COH_PATH_OUT,SRC)
        tiff_path = os.path.join(coh_path,SRC.split('.')[0]+'_tiff')
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
            print(out_path)
            os.system("python ParseBrownian.py -PSF {} -out {} -width 75 -height 75 -every 25 {} {}".format(PSF_FILE,out_path,SRC_path,file_path))
        if not os.path.isdir(tiff_path):
            os.mkdir(tiff_path)
            os.system("python BrownianXMLtoTIFF.py -green -out {} {}".format(tiff_path,out_path))
