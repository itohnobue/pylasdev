import numpy

def compare_las_dicts(old, new):
	for key in new.keys():

		# check that old one have the key
		if key not in old:
			print "Error! ", key, " key not found in the 2nd dict."
			return False

		# parsing internal dict
		if(type(new[key]) is dict):

			for in_key in new[key].keys():
				# comparing numpy arrays
				if type(new[key][in_key]) is numpy.ndarray:	

					# size compare
					if old[key][in_key].size != new[key][in_key].size:
						print "Error! Numpy arrays sizes in 1st and 2nd dicts are not the same: ", key, in_key
						return False

					# values compare
					if not all(old[key][in_key] == new[key][in_key]):
						print "Error!  Numpy arrays values in 1st and 2nd dicts are not the same: ", key, in_key
						print "1st dict values: ", [ old[key][in_key] ]
						print "2nd dict values: ", [ new[key][in_key] ]
						return False
				else:
					# any other type
					if old[key][in_key] != new[key][in_key]:
						print "Error! Internal dict ", key, " not the same in 1st and 2nd dicts."
						print "1st dict value: ", [ old[key][in_key] ]
						print "2nd dict value: ", [ new[key][in_key] ]
						return False
		# internal non-dicts
		else:
			if type(new[key]) is numpy.ndarray:

					# size compare
					if old[key].size != new[key].size:
						print "Error! Numpy arrays sizes in 1st and 2nd dicts are not the same: ", key
						return False

					# values compare
					if not all(old[key] == new[key]):
						print "Error!  Numpy arrays values in 1st and 2nd dicts are not the same: ", key
						print "1st dict values: ", [ old[key] ]
						print "2nd dict values: ", [ new[key] ]
						return False
			else:
				if old[key] != new[key]:
					print "Error! Not matched: ", key
					print "1st dict value: ", [ old[key] ]
					print "2nd dict value: ", [ new[key] ]
					return False

	# everything is ok :)
	return True



# Test

"""
dict1 = {}
dict2 = {}

dict1['A'] = 'A'
dict1['B'] = 'B'
dict1['C'] = 'C'

dict2['A'] = 'A'
dict2['B'] = 'B'
dict2['C'] = 'C'

dict1['D1'] = {}
dict2['D1'] = {}

dict1['D1']['A'] = 'A'
dict2['D1']['A'] = 'B'

dict1['D1']['AR'] = numpy.array([1,2,3,5])
dict2['D1']['AR'] = numpy.array([1,2,3,2])

print compare_las_dicts(dict1, dict2)
"""

