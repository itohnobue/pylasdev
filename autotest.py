from pylasdev import *
import pickle

# Autotest for Wells module

las_test_files = [

	# LAS 1.2

	"test_data/sample.las",			# OK
	"test_data/sample_minimal.las",		# OK
	"test_data/sample_wrapped.las",		# OK
	"test_data/sample_curve_api.las",	# OK
#	"test_data/sample_big.las",		# 2 Mb - OK -- no pickle test
#	"test_data/sample_very_big.las", 	# 12 Mb - OK -- no pickle test

	# LAS 2.0

	"test_data/sample_2.0.las", 		# OK
	"test_data/sample_2.0_minimal.las", 	# OK
	"test_data/sample_2.0_wrapped.las",	# OK
	"test_data/sample_2.0_based.las", 	# OK 

	"test_data/petrel2.0.las", 		# OK 
]

dev_test_files = [

	"test_data/sample.dev"
]


# Write new pickle files (uncomment to make new pickled files)

"""
print "Writing .pickle files..."

# LAS

for file in las_test_files:
	las_info = read_las_file(file)
	output_file = open('pickled_' + file + '.pickle', 'wb')
	pickle.dump(las_info, output_file)
	output_file.close()

# DEV

for file in dev_test_files:
	dev_info = read_dev_file(file)
	output_file = open('pickled_' + file + '.pickle', 'wb')
	pickle.dump(dev_info, output_file)
	output_file.close()
"""

# Load and test with pickled data

# LAS

for file in las_test_files:
	print "Testing", file, "..."
	las_info = read_las_file(file)
	pkl_file = open('pickled_' + file + '.pickle', 'rb')
	las_info_pkl = pickle.load(pkl_file)
	pkl_file.close()

	if (compare_las_dicts(las_info_pkl, las_info)):
		print "OK."
	else:
		print "ERROR!"

# DEV

for file in dev_test_files:
	print "Testing", file, "..."
	dev_info = read_dev_file(file)
	pkl_file = open('pickled_' + file + '.pickle', 'rb')
	dev_info_pkl = pickle.load(pkl_file)
	pkl_file.close()

	if (compare_las_dicts(dev_info_pkl, dev_info)):
		print "OK."
	else:
		print "ERROR!"

# LAS Writer Test

for file in las_test_files:
        print "Testing writing for ", file, "..."

        las_info = read_las_file(file)
	write_las_file(file + ".writed", las_info)
        las_info_writed = read_las_file(file + ".writed")

#	print las_info
#	print las_info_writed

	if (compare_las_dicts(las_info_writed, las_info)):
		print "OK."
	else:
		print "ERROR!"

