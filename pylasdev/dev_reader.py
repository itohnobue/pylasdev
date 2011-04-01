import re
import numpy

# Wells Path/Deviation file reader

def read_dev_file(filename):

	# -----

	# Pre-calc for lines counting and arrays pre-init

	file = open(filename)

	lines_count = -1 # minus data names line

	while 1:

		lines = file.readlines(100000)

		if not lines:
			break
		for line in lines:
			line = line.lstrip()
			if len(line) > 0:		# skipping empty line
				if line[0] != '#':	# skipping comment line
					lines_count += 1
	file.close()

	# ---

	# Actual reading

	file = open(filename)
	header_line_founded = False

	dev_dict = {}
	names = []

	current_data_line = 0

	while 1:

		lines = file.readlines(100000)

		if not lines:
			break
		for line in lines:
			line = line.lstrip()
			if len(line) > 0:		# skipping empty line
				if line[0] != '#':	# skipping comment line
					line = re.sub(r'\n','',line)		# remove \n
					line = line.lstrip()			# remove whitespaces from the beginning
					values = re.split(r'[ \t]+', line)	# split line in tokens by spaces and tabs
		
					if header_line_founded == False:
						names = values
						for name in values:
							# dev_dict[name] = numpy.array([])
							dev_dict[name] = numpy.zeros(lines_count)
						header_line_founded = True	
					else:
						for k in xrange(len(values)):
							dev_dict [ names[k] ][current_data_line] = float(values[k])
						current_data_line += 1
	return dev_dict


