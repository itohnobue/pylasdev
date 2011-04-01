import ply.lex as lex
import ply.yacc as yacc
import re
import numpy

las_info = {}

parse_error = True 

las_info['version'] = {}
las_info['well'] = {}
las_info['parameters'] = {}
las_info['logs'] = {}
las_info['curves_order'] = []

# Lexer

tokens = (
	'SYMBOL',
	'DOT',
	'COLON',
	'WS',
	'TILD',
	'SHARP',
	'BAR'
)

t_SYMBOL = r'[a-zA-Z0-9\-\]\[]'
t_DOT = r'\.'
t_COLON = r':'
t_WS = r'[\s\t]+'
t_TILD = r'~'
t_SHARP = r'\#'
t_BAR = r'\|'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ''

def t_error(t):
#	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

# Parser

start = "line"

def p_line(t):
	"""line : opt_wss name wss value COLON opt_wss comment
		| opt_wss name wss COLON opt_wss comment
		| opt_wss name wss value COLON opt_wss 
		| opt_wss name wss value
		| opt_wss name wss COLON opt_wss comment BAR opt_wss second_part opt_wss
		| opt_wss name wss value COLON opt_wss comment BAR opt_wss second_part opt_wss
		| opt_wss name wss value COLON opt_wss BAR opt_wss second_part opt_wss
		| opt_wss name wss value BAR opt_wss second_part opt_wss
		| caption
		| empty
		
	"""

	if t[1] == None:	# empty line
		pass

	if len(t) == 2:		# caption of the section
		if(t[1][0] == '~'):
			las_info['version']['last_caption'] = t[1]
	elif las_info['version']['last_caption'][:2] == '~C': # curve section
		t[2] = re.sub("\s+", "", t[2])
#		if re.sub(r'\s+','',las_info['version']['WRAP']) == 'NO':
#			las_info['logs'][ t[2] ] = numpy.zeros(lines_count)
#		else:
#			las_info['logs'][ t[2] ] = numpy.array([])
		las_info['curves_order'].append( t[2] )
	elif las_info['version']['last_caption'][:2] == '~V': # version section
		t[2] = re.sub("\s+", "", t[2])
		t[4] = re.sub(' ', '', t[4])

		las_info['version'][t[2]] = t[4]

		if(t[2] == 'WRAP' and t[4] == 'YES'):
			print "Warning! WRAP mode not allowed in LAS 3.0 specification. Reading file as non-WRAPped..."

		if(t[2] == 'DLM'):
			if t[4] != 'SPACE' and t[4] != 'COMMA' and t[4] != 'TAB':
				print "Error! Unknown DLM value: ", t[4], "(Must be SPACE, COMMA or TAB)"
				global parse_error
				parse_error = False 

		# TODO: find out what DLM format will be used 

#		if(t[2] == 'DLM'):
#			if(t[4] == 'SPACE'):
#				las_info['version']['DLM'] = ' '
#			elif(t[4] == 'COMMA'):
#				las_info['version']['DLM'] = '.'
#			elif(t[4] == 'TAB'):
#				las_info['version']['DLM'] = '.'


	elif las_info['version']['last_caption'][:2] == '~W': # well section
		t[2] = re.sub("\s+", "", t[2])
		t[4] = t[4].lstrip().rstrip()
		if(t[4] == ':'):
			las_info['well'][t[2]] = ''
		else:
			las_info['well'][t[2]] = t[4]
	elif las_info['version']['last_caption'][:2] == '~P': # parameters section
		t[2] = re.sub("\s+", "", t[2])
		t[4] = t[4].lstrip().rstrip()
		if len(t) == 8:
			for tok in t: print tok
			las_info['parameters'][t[6]][t[2]] = t[4]
		elif len(t) == 10:
			las_info['parameters'][t[8]][t[2]] = t[4]
		elif len(t) == 11:
			las_info['parameters'][t[9]][t[2]] = t[4]
		else:
			las_info['parameters'][t[2]] = t[4]
#	elif las_info['version']['last_caption'] == '~O': # other section
#		pass

def p_optional_wss(t):
	"""opt_wss : wss 
		| empty"""
	t[0] = t[1]
#	print "OWSS", t[0]


def p_name(t):
	"""name : first_part DOT second_part 
		| first_part DOT"""
#	if (len(t) == 4):
#		t[0] = t[1] + t[2] + t[3]
#	else:
#		t[0] = t[1] + t[2]
	t[0] = t[1]
#	print "N", t[0]

def p_first_part(t):
	"""first_part : first_part first_part_term 
				  | SYMBOL"""
	if len(t) == 3:
		t[0] = t[1] + t[2]
	else:
		t[0] = t[1]
#	print "FP", t[0]

def p_first_part_term(t):
	"""first_part_term : SYMBOL 
		| WS"""
	t[0] = t[1]

#def p_line_comment(t):
#	"""line_comment : anys
#		| caption anys"""
#	pass

def p_second_part(t):
	"""second_part : second_part SYMBOL 
		| SYMBOL"""
	if len(t) == 3:
		t[0] = t[1] + t[2]
	else:
		t[0] = t[1]
#	print "SP", t[0]

def p_wss(t):
	"""wss : wss WS 
		| WS"""
	if len(t) == 3:
		t[0] = t[1] + t[2]
	else:
		t[0] = t[1]
#	print "WSS", t[0]


def p_value(t):
	"""value_1 : SYMBOL 
		| DOT
	   value_rest : SYMBOL 
		| DOT 
		| WS
	   value : value value_rest
			 | value_1"""
	if len(t) == 3:
		t[0] = t[1] + t[2]
	else:
		t[0] = t[1]
#	print "VL ", t[0]

def p_comment(t):
	"""comment_symbol_1 : SYMBOL
		| DOT
	comment_symbol : SYMBOL 
		| DOT 
		| WS 
		| COLON
		| SHARP
	   comment : comment comment_symbol 
			   | comment_symbol_1"""
	if len(t) == 3:
		t[0] = t[1] + t[2]
	else:
		t[0] = t[1]
#	print "COMMENT ", t[0]


def p_empty(t):
	'empty :'
	pass


def p_caption(t):
	'caption : TILD comment'
	t[0] = t[1] + t[2]

def p_error(t):
	print "Syntax error at '%s'" % t
#	print t.lexpos, t.type

lexer = lex.lex()
yacc.yacc(start="line")

def parse_line(line, l_count):
	global lines_count
	lines_count = l_count
	lexer.input(line)
	yacc.parse(line)
	return parse_error
