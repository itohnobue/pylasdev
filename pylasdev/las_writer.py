
def write_las_file(filename, las_dict):

	file = open(filename, "w")
	
	# 1. Version section

	file.write("~VERSION INFORMATION\n")

	file.write(" VERS. " + las_dict['version']['VERS'] + "  : X\n")
	file.write(" WRAP. " + las_dict['version']['WRAP'] + "  : X\n")

	# 2. Well section
	
	file.write("~WELL INFORMATION\n")

	for key in las_dict['well'].keys():
		file.write(" " + key + ".X  " + las_dict['well'][key] + "  : X\n")

	# 3. Curve section

	file.write("~CURVE INFORMATION\n")
	
	for k in xrange(len(las_dict['curves_order'])):
		file.write(" " + las_dict['curves_order'][k] + ".X  : X \n")

	# 4. Parameters section

	file.write("~PARAMETERS INFORMATION\n")
	
	for key in las_dict['parameters'].keys():
		file.write(" " + key + ".X  " + las_dict['parameters'][key] + "  : X\n")

	# 5. Logs

	size = -1

	# Header	

	file.write("~A")
	
        for k in xrange(len(las_dict['curves_order'])):
                file.write("  " + las_dict['curves_order'][k])
		if(size == -1):
			size = las_dict['logs'][las_dict['curves_order'][k]].size

	file.write("\n")

	# Values
#	print size
#	for key in las_dict['curves_order']:
#		print key, las_dict['logs'][key].size

	for i in xrange(size):
		for key_ordered in las_dict['curves_order']:
#			print key_ordered
#			print las_dict['logs'][key_ordered]
#			print i
			file.write("  " + str(las_dict['logs'][key_ordered][i]))
		file.write("\n")

	file.close()
