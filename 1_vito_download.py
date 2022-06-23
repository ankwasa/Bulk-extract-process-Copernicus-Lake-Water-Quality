# usr/bin/env-python3

'''

this script bulk downloads  VITO -Lake water quality
Author  : albert nkwasa
Contact : nkwasa.albert@gmail.com / albert.nkwasa@vub.be 
Date    : 2022.06.23


'''

#           VITO -Lake water quality - downloading
from ftplib import FTP
import os
import os.path
import shutil

# directory = os.path.dirname(os.path.realpath(__file__))
directory = os.getcwd()
dir_input_maps = directory + "\\vito_download"
os.chdir(dir_input_maps)
ftp = FTP('ftp.copernicus.vgt.vito.be')

# -------------------------------------------------------
# - - - USER INPUT - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------
username = input("Provide your username: ")
pswrd = input("Provide your password: ")
print('Logging in.')
ftp.login(username, pswrd)

# and provide ftp directory.
vito_download = input(
    'Provide order name given in the email from VITO (mailing@vito.be) for example M0169702) : ')

# -------------------------------------------------------
# - - - DOWNLOADING - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------
ftp.cwd(vito_download)
ftp.retrlines('LIST')
print('Downloading files')

filenames = ftp.nlst()
folder_list = []
for i in filenames:
    all_list = ftp.nlst(i)
    folder_list.append(all_list)

for name in folder_list:
    for i in name:
        # print(i[44:])
        local_filename = os.path.join(dir_input_maps, i[44:])
        print(local_filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + i, file.write)
        file.close()
ftp.quit()

print("\t > Downloading complete.")

'''unzipping files'''

os.system('python 2_unzipping_files.py')
os.system('python 3_grouping_files.py')
