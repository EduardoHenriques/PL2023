import ply.lex as lex
import sys
import re


def t_error(t):
	print("Caracter ilegal: ", t)
	t.lexer.skip(1)


if __name__ == "__main__":
	tokens = [
		'openCurlyBracket',
		'closeCurlyBracket',
		'prog',
		'func',
		'var',
		'list',
		'newline',
		'space',
		'singleComm',
		'multCommOpen',
		'multCommClose',
		'multComm',
		'word',
		'if',
		'assign',
		'declare',
		'openBoxBracket',
		'closeBoxBracket',
		'openCurveBracket',
		'closeCurveBracket'
	]

	t_singleComm = r'\/\/'
	t_newline = r'\n'
	t_space = r'\ '

	t_openCurlyBracket = r'\{'
	t_closeCurlyBracket = r'\}'

	t_openCurveBracket = r'\('
	t_closeCurveBracket = r'\)'

	t_openBoxBracket = r'\['
	t_closeBoxBracket = r'\]'

	t_var = r'int|float|double'  # int
	t_declare = t_var + t_space + r'+[a-zA-Z][a-zA-z\d_]*'  # int i
	t_assign = t_var + t_space + r'+[a-zA-Z][a-zA-z\d_]*' + r'\s*=\s*' + r'\d+'  # int i = 1

	t_if = r'\s?if'

	t_word = r'.+'
	t_multCommOpen = r'/\*'
	t_multCommClose = r'\*/'
	t_multComm = t_multCommOpen + t_word + r'\+' + t_multCommClose

	t_ignore = r'^.+$'

	lexer = lex.lex()

	if __name__ == "__main__":
		n_teste = input("Teste numero:")
		pwd = "teste" + n_teste + ".txt"
		with open(pwd, 'r') as file:
			lines = file.readlines()
			print(len(lines))
			for line in lines:
				lexer.input(line)
				for token in lexer:
					if token.type != "newline" and token.type != "space":
						print(token.type + " | " + token.value)
