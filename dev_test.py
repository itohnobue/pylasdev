from pylasdev import *
from mnem_base import *

# Simple test for Wells Path/Dev file reader

test_files = [

	"test_data/sample.dev",
]

file = test_files[0]

print "Reading file ", file, " ..."

dev_info = read_dev_file(file)

print "Done."

if(dev_info is None):
	print "Error, file not readed!"
else:
	for key in dev_info.keys():
		print "  ", [key], [dev_info[key]]

