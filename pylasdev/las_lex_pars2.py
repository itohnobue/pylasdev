# -*- coding: utf-8 -*- 

import ply.lex as lex
import ply.yacc as yacc
import re
import numpy


# This is a Lexer and Parser for LAS 1.2/2.0 files header

las_info = {}
gmnem_base = None

las_info['version'] = {}
las_info['well'] = {}
las_info['parameters'] = {}
las_info['logs'] = {}
las_info['curves_order'] = []

# -- Lexer

tokens = (
	'SYMBOL',
	'DOT',
	'COLON',
	'WS',
	'TILD',
	'SHARP'
)

t_SYMBOL = r'(?u)[А-Яа-яa-zA-Z0-9\-]'
t_DOT = r'\.'
t_COLON = r':'
t_WS = r'[\s\t]+'
t_TILD = r'~'
t_SHARP = r'\#'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ''

def t_error(t):
#	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

# -- Parser

start = "line"

def p_line(t):
	"""line : opt_wss name wss value COLON opt_wss comment
		| opt_wss name wss COLON opt_wss comment
		| opt_wss name wss value COLON opt_wss 
		| opt_wss name wss value
		| caption
		| empty
		
	"""

	if t[1] == None:	# empty line
		pass

	if len(t) == 2:		# caption of the section
		if(t[1][0] == '~'):
			las_info['version']['last_caption'] = t[1]
	
	elif las_info['version']['last_caption'] == '~C': # curve section
		t[2] = re.sub("\s+", "", t[2])

		if gmnem_base is not None:
			if(gmnem_base.has_key(t[2])):
#				print "Curve name ", t[2], " founded in mnemonics database... Replacing with ", gmnem_base[ t[2] ]
				t[2] = gmnem_base[ t[2] ]

		las_info['curves_order'].append( t[2] )


		if re.sub(r'\s+','',las_info['version']['WRAP']) == 'NO':
			las_info['logs'][ t[2] ] = numpy.zeros(lines_count)
		else:
			las_info['logs'][ t[2] ] = numpy.array([])


	elif las_info['version']['last_caption'] == '~V': # version section
		t[2] = re.sub("\s+", "", t[2])
		las_info['version'][t[2]] = t[4].lstrip().rstrip()

	elif las_info['version']['last_caption'] == '~W': # well section
		t[2] = re.sub("\s+", "", t[2])
		t[4] = t[4].lstrip().rstrip()

		if t[4] == ':':
			# empty value case
			las_info['well'][t[2]] = ''
		else:
			las_info['well'][t[2]] = t[4]

	elif las_info['version']['last_caption'] == '~P': # parameters section
		t[2] = re.sub("\s+", "", t[2])
		t[4] = t[4].lstrip().rstrip()
		if t[4] == ':':
			# empty value case
			las_info['parameters'][unicode(t[2])] = ''
		else:
			las_info['parameters'][unicode(t[2])] = t[4]

	elif las_info['version']['last_caption'] == '~O': # other section
		pass

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
		| SHARP
	   value_rest : SYMBOL 
		| DOT 
		| WS
		| SHARP
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
		| SHARP
		| empty
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
	t[0] = t[1] + t[2][0]

def p_error(t):
	print "Syntax error at '%s'" % t
#	print t.lexpos, t.type

lexer = lex.lex(reflags=re.UNICODE)
yacc.yacc(start="line")

# We need this function to know the number of lines in file inside of the parser (for ASCII LOGS arrays initialization in !wrapped mode)

def parse_line(line, l_count, mnem_base):
	global lines_count
	lines_count = l_count
	global gmnem_base
	gmnem_base = mnem_base
	lexer.input(line)
	yacc.parse(line)
