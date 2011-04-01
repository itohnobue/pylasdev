
# LAS Well Logs ver. 1.2/2.0 files reader


# ASCII LOGS section line parser
from las_line_reader import *

# Lexer and parser for LAS 1.2/2.0 format
import las_lex_pars2 as las2

#import time

def read_las_file(filename, mnem_base = None):

	# --- First run

	# We need this to check how many ASCII LOGS lines file has (for array pre-initialization in wrapped mode)
	# and to check the LAS version

	las2.las_info['version'] = {}
	las2.las_info['version']['last_caption'] = '~V'
	las2.las_info['well'] = {}
	las2.las_info['parameters'] = {}
	las2.las_info['logs'] = {}
	las2.las_info['curves_order'] = []

	file = open(filename)

#	time1 = time.time()

	lines_count = 0

	ascii_logs_section = False
	version_section = False

	while 1:

		lines = file.readlines(100000)

		if not lines:
			break
		for line in lines:
			line = line.lstrip()
			if len(line) > 0:		# skipping empty line
				if line[0] != '#':	# skipping comment line
					if ascii_logs_section == True:	# founded ASCII LOGS line
						lines_count += 1
					elif version_section == True:	# we are in VERSION section
						if line[0] == '~':
							version_section = False	# VERSION section ended
						else:
							las2.lexer.input(line)	# checking LAS version
							las2.yacc.parse(line)
					else:
						if line[:2] == '~A':	# found the ASCII LOGS section
							ascii_logs_section = True
						elif line[:2] == '~V':	# found the VERSION section
							version_section = True
	file.close()

	# -- Second run

	# Now we parse and read!

#	time2 = time.time()
#	print "Precalc time is: ", time2 - time1
#	time1 = time.time()

	# Checking LAS version and choosing the right lexer/parser pair
	# for future use, LAS 3.0 not implemented yet

	if float(las2.las_info['version']['VERS']) < 3.0:
		import las_lex_pars2 as las_lex_pars
	else:
		#import las_lex_pars3 as las_lex_pars
		print "Sorry, LAS version > 2.0 is not supported."
		return None

	# input structure initialization

	las_lex_pars.las_info['version'] = {}
	las_lex_pars.las_info['version']['last_caption'] = '~V'
#	las_lex_pars.las_info['version']['DLM'] = 'SPACE'
	las_lex_pars.las_info['well'] = {}
	las_lex_pars.las_info['parameters'] = {}
	las_lex_pars.las_info['logs'] = {}
	las_lex_pars.las_info['curves_order'] = []


	file = open(filename)

	lr_obj = line_reader()	# initializing ASCII LOGS lines reader object
	other_section = False
	ascii_logs_section = False

	while 1:

		lines = file.readlines(100000)

		if not lines:
			break
		for line in lines:
			line = line.lstrip()
			if len(line) > 0 :	# empty line
				if line[0] != '#':	# comment line
				
					# are we in ASCII Logs section?
					if ascii_logs_section == True:
						pass
						# if it is, let's parse the log line
						lr_obj.read_line(line, las_lex_pars.las_info)
					# if not, let's check out, maybe it had started just now
					elif line[:2] == '~A':
						ascii_logs_section = True
					# all right, that's not an ASCII Logs section, go ahead
					else:
						# let's check that we are not in Other section
						if other_section == True:
							# if it is, check - maybe it had ended just now
							if line[0] == '~':
								other_section = False
						else:
							# ok, we are not in Other section, let's check - maybe it is ahead
							if line[:2] == '~O':
								other_section = True
							# nope - OK! we are in header, let's parse :)
							else:
								# Parsing Header
								if(las_lex_pars.parse_line(line, lines_count, mnem_base) == False):
									return None


	#time2 = time.time()

	#print "Parsing time is: ", time2 - time1

	return las_lex_pars.las_info
