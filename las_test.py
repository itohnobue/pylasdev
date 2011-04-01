from pylasdev import *
#from mnem_base import *

# Simple test with full LAS output for LAS reader

test_files = [

	# LAS 1.2

	"test_data/sample.las",			# 0 - OK
	"test_data/sample_minimal.las",		# 1 - OK
	"test_data/sample_wrapped.las",		# 2 - OK
	"test_data/sample_curve_api.las",	# 3 - OK

#	"test_data/sample_big.las",		# 2 Mb - OK -- no pickle test
#	"test_data/sample_very_big.las", 	# 12 Mb - OK -- no pickle test

	# LAS 2.0

	"test_data/sample_2.0.las", 		# 4 - OK
	"test_data/sample_2.0_minimal.las", 	# 5 - OK
	"test_data/sample_2.0_wrapped.las",	# 6 - OK
	"test_data/sample_2.0_based.las", 	# 7 - OK 

	"test_data/petrel2.0.las", 		# 8 -OK

    "test_data/5_1.las",    # andrey converter # 9 - OK
    "test_data/4ALS.las",   # nadezhdin's output # 10 - OK
    "test_data/1475IBK3.las" # bashneft cp866 # 11

#	"test_data/comment_test.las",

	# LAS 3.0 # not implemented

#	"test_data/sample_3.0.las", 		#

]

file = test_files[4]

print "Reading file ", file, " ..."

#las_info = read_las_file(file, mnem_base)
las_info = read_las_file(file)

print "Done."

if(las_info is None):
	print "Error, file not readed!"
else:
	print "=== Version: "
	for key in las_info['version'].keys():
		print "  ", [key], [las_info['version'][key]]

	print "=== Well:"
	for key in las_info['well'].keys():
		print "  ", [key], [las_info['well'][key]]

	print "=== Parameters:"
	for key in las_info['parameters'].keys():
		print "  ", [key], [las_info['parameters'][key]]

	print "=== Curves:"
	for k in xrange(len(las_info['curves_order'])):
		print "  ", k, las_info['curves_order'][k]

	print "=== Logs:"
	for key_ordered in las_info['curves_order']:
		print "  ", [key_ordered], [las_info['logs'][key_ordered]]


# writing test

#filename = "write_test.las"
#write_las_file(filename, las_info)

