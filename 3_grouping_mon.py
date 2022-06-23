# usr/bin/env-python3

'''

this script groups the LWQ into monthloy and longterm monthly raster images
Author  : albert nkwasa
Contact : nkwasa.albert@gmail.com / albert.nkwasa@vub.be 
Date    : 2022.06.23


'''

import os
from osgeo import gdal
import numpy as np
import pandas as pd
import warnings
import shutil


warnings.filterwarnings(action='ignore', message='Mean of empty slice')

rootdir = os.getcwd()

dir_trophic = rootdir + '\\tropic_state_index'
dir_turbidity = rootdir + '\\turbidity_mean'
dir_trophic_mon = rootdir + '\\monthly_trophic_state'
dir_turbidity_mon = rootdir + '\\monthly_turbidity'
dir_input_trophic = rootdir + '\\ref_trophic.tiff'
dir_input_turbidity = rootdir + '\\ref_turbidity.tiff'
dir_agg_trophic = rootdir + '\\agg_trophic'
dir_agg_turbidity = rootdir + '\\agg_turbidity'

# copy ref tiff files
rootdir = os.getcwd()

tropic_state = []
for subdir, dirs, files in os.walk(rootdir):
    tropic_state.append(subdir)

for k in os.listdir(tropic_state[1]):
    if k.startswith('c_gls_LWQ300-trophic-state-index'):
        try:
            shutil.copy2(k, rootdir + '\\ref_trophic.tiff')
        except:
            pass
    if k.startswith('c_gls_LWQ300-turbidity-mean'):
        try:
            shutil.copy2(k, rootdir + '\\ref_turbidity.tif')
        except:
            pass
# functions


def SearchFolder(directory, file_format):
    MyFolder = os.listdir(directory)
    MyList = []
    a = len(file_format)
    for b in range(len(MyFolder)):
        i = MyFolder[b]
        if i[-a:] == file_format:
            MyList.append(MyFolder[b])
    return MyList


def LAI_Map_Agg(in_raster, output_folder, filename, month, year, ref_tif, parameter, low_limit, upp_limit):
    list_of_maps = []
    for i in filename:
        if i[low_limit:upp_limit] == year+month:
            list_of_maps.append(i)
# looping through selected month and year!
    if len(list_of_maps) == 0:
        pass
    else:
        # create i - dimentional matrix per month
        LAI_maps = []
        for i in range(len(list_of_maps)):
            data_src = gdal.Open(in_raster + "\\" + list_of_maps[i] + ".tiff")
            read_file = data_src.GetRasterBand(1).ReadAsArray()
            copy_map = read_file.copy()
            no_data = 9.96921e+36
            copy_map[copy_map == no_data] = np.nan
            LAI_maps.append(copy_map)

        stacked = np.dstack(LAI_maps)
        mean = np.nanmean(stacked, axis=-1)

        os.chdir(output_folder)
        name = list_of_maps[0]
        date = name[low_limit:upp_limit]
        image_output = output_folder + "\\" + \
            str(date) + "_Monthly_{}.tiff".format(parameter)

        driver = gdal.GetDriverByName('GTiff')
        result = driver.CreateCopy(image_output, gdal.Open(ref_tif))
        result.GetRasterBand(1).WriteArray(mean)
        result = None

    return list_of_maps


print('\nGenerating monthly aggregated Trophic.tif maps... ')
Myfiles5 = SearchFolder(dir_trophic, '.tiff')
data_src = gdal.Open(dir_trophic + "\\" + Myfiles5[0])
band_info = data_src.GetRasterBand(1)
filenames = []
dates = []
for i in range(len(Myfiles5)):
    breakList = Myfiles5[i].split("\\")
    fn = breakList[-1]
    fn = fn[:-5]
    filenames.append(fn)
    fn2 = fn.split("_")
    fn2 = fn2[3]
    dates.append(fn2)
# print(dates)
# print(filenames)
years = []
months = ['01', '02', '03', '04', '05',
          '06', '07', '08', '09', '10', '11', '12']
for j in range(len(dates)):
    date = dates[j]
    year = date[:4]
    if year not in years:
        years.append(year)
in_raster = dir_trophic
out_raster = dir_trophic_mon
# print(years)
print('\nStatus report - number of available products for each month')
os.chdir(dir_trophic_mon)
report = open('report.txt', 'w')
for i in range(len(years)):
    report.write('\n ===================================================== ')
    report.write(
        '\n List of maps used for aggregation in the YEAR: ' + str(years[i]) + '\n')
    name_of_months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
    for k in range(12):
        add_list = LAI_Map_Agg(in_raster, out_raster,
                               filenames, months[k], years[i], dir_input_trophic, 'trophic', 33, 39)
        try:
            if len(add_list) != 0:
                print(add_list)
                report.write('\n ' + str(name_of_months[k]) + ':')
                for a in add_list:
                    b = ' ' + str(a)
                    report.write(b)
        except:
            pass
report.write(' ===================================================== ')
report.close()


print('\n >Generating monthly aggregated Turbidity.tif maps... ')
Myfiles5 = SearchFolder(dir_turbidity, '.tiff')
data_src = gdal.Open(dir_turbidity + "\\" + Myfiles5[0])
band_info = data_src.GetRasterBand(1)
filenames = []
dates = []
for i in range(len(Myfiles5)):
    breakList = Myfiles5[i].split("\\")
    fn = breakList[-1]
    fn = fn[:-5]
    filenames.append(fn)
    fn2 = fn.split("_")
    fn2 = fn2[3]
    dates.append(fn2)
# print(dates)
# print(filenames)
years = []
months = ['01', '02', '03', '04', '05',
          '06', '07', '08', '09', '10', '11', '12']
for j in range(len(dates)):
    date = dates[j]
    year = date[:4]
    if year not in years:
        years.append(year)
in_raster = dir_turbidity
out_raster = dir_turbidity_mon
# print(years)
print('\nStatus report - number of available products for each month')
os.chdir(dir_turbidity_mon)
report = open('report.txt', 'w')
for i in range(len(years)):
    report.write('\n ===================================================== ')
    report.write(
        '\n List of maps used for aggregation in the YEAR: ' + str(years[i]) + '\n')
    name_of_months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
    for k in range(12):
        add_list = LAI_Map_Agg(in_raster, out_raster,
                               filenames, months[k], years[i], dir_input_turbidity, 'turbidity', 28, 34)
        try:
            if len(add_list) != 0:
                print(add_list)
                report.write('\n ' + str(name_of_months[k]) + ':')
                for a in add_list:
                    b = ' ' + str(a)
                    report.write(b)
        except:
            pass
report.write(' ===================================================== ')
report.close()

# Aggregating the months


def agg_month(path_monthly_files, output_dir, ref_tif, parameter):
    MonthlyFiles = os.listdir(path_monthly_files)
    MyList_monthly = []
    a = len('tiff')
    for b in range(len(MonthlyFiles)):
        i = MonthlyFiles[b]
        if i[-a:] == 'tiff':
            MyList_monthly.append(MonthlyFiles[b])

    filenames_monthly = []
    for i in range(len(MyList_monthly)):
        # Need to confirm the file format.
        breakList = MyList_monthly[i].split("\\")
        fn = breakList[-1]
        fn = fn[:-5]
        filenames_monthly.append(fn)

    for k in range(12):
        list_of_maps_agg = []
        for i in filenames_monthly:
            if i[4:6] == months[k]:
                list_of_maps_agg.append(i)
    # looping through selected month and year!
        if len(list_of_maps_agg) == 0:
            pass
        else:
            # create i - dimentional matrix per month
            LAI_maps_agg = []
            for m in range(len(list_of_maps_agg)):
                data_src = gdal.Open(path_monthly_files +
                                     "\\" + list_of_maps_agg[m] + ".tiff")
                read_file = data_src.GetRasterBand(1).ReadAsArray()
                copy_map = read_file.copy()
                no_data = 9.96921e+36
                copy_map[copy_map == no_data] = np.nan
                LAI_maps_agg.append(copy_map)

            stacked = np.dstack(LAI_maps_agg)
            mean = np.mean(stacked, axis=-1)
            # mean = np.mean(np.array(LAI_maps), axis=0)

            os.chdir(output_dir)
            image_output = output_dir + "\\" + \
                months[k] + "_{}.tif".format(parameter)

            driver = gdal.GetDriverByName('GTiff')
            result = driver.CreateCopy(image_output, gdal.Open(ref_tif))
            result.GetRasterBand(1).WriteArray(mean)
            result = None


agg_month(dir_trophic_mon, dir_agg_trophic, dir_input_trophic, 'trophic')
agg_month(dir_turbidity_mon, dir_agg_turbidity,
          dir_input_turbidity, 'turbidity')
print('\t > finished')
