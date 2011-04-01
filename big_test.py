from pylasdev import *
from mnem_base import mnem_base
import os
import time
import scipy.io as io

rootdir = 'test_data'
outdir = 'mat_files'

dev_files = []
las_files = []

counter = 0
full_size = 0

time_begin = time.time()

for dirpath, dirnames, files in os.walk(rootdir):
    for file in files:
		
        fullpath = os.path.join(dirpath, file)

        file_size = os.path.getsize(fullpath) / 1024

        if fullpath.split('.')[1] == 'las':

            print "Reading", file, "...", "[", file_size, " Kb]"

            las_readed = read_las_file(fullpath, mnem_base)
            las_files.append(las_readed)

            las_prepared = {}

            print "  Saving as MATLAB file..."

            for key_ordered in las_readed['curves_order']:
                las_prepared[key_ordered] = las_readed['logs'][key_ordered]

            io.savemat(os.path.join(outdir, file + ".mat"), las_prepared)

            print "  Done."

            full_size += file_size
            counter +=1

time_end = time.time()

print counter, "files [", full_size / 1024 ,"Mb ] readed in", time_end - time_begin, "seconds"

