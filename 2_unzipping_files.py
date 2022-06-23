# usr/bin/env-python3


import os
import zipfile
import shutil

rootdir = os.getcwd()
extension = ".zip"

os.chdir(rootdir)  # change directory from working dir to dir with files

# Unzip the files
for item in os.listdir(rootdir):  # loop through items in dir
    if item.endswith(extension):  # check for ".zip" extension
        file_name = os.path.abspath(item)
        try:   # get full path of files
            zip_ref = zipfile.ZipFile(file_name)
            # create zipfile object
            zip_ref.extractall(rootdir)  # extract file to dir
            zip_ref.close()  # close file
            os.remove(file_name)  # delete zipped file
        except:
            pass


# make new directories
try:
    os.makedirs('tropic_state_index')
    os.makedirs('turbidity_mean')
    os.makedirs('monthly_trophic_state')
    os.makedirs('monthly_turbidity')
    os.makedirs('agg_turbidity')
    os.makedirs('agg_trophic')
except:
    pass


# Sort the files
tropic_state = []
turbidity = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.startswith('c_gls_LWQ300-trophic-state-index'):
            tropic_state.append(os.path.join(subdir, file))
        if file.startswith('c_gls_LWQ300-turbidity-mean'):
            turbidity.append(os.path.join(subdir, file))
try:
    for k in tropic_state:
        shutil.copy2(k, rootdir + '\\tropic_state_index')
    for j in turbidity:
        shutil.copy2(j, rootdir + '\\turbidity_mean')
except:
    pass
