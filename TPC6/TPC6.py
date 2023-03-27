import ply.lex as lex



def t_error(t):
	# print("Caracter ilegal: ", t)
	t.lexer.skip(1)


if __name__ == "__main__":
	tokens = [
		'prog', 'declareFunc', 'callFunc',

		'args', 'var', 'dig', 'num',

		'newline', 'endline', 'space', 'comma',

		'singleComm', 'multCommOpen', 'multCommClose', 'multComm',

		'if', 'for', 'in', 'to', 'while',

		'equals', 'bigger', 'smaller',
		'plus',	'minus', 'times', 'div',

		'declareInt', 'declareFloat', 'declareDouble',	# int x;
		'assignInt', 'assignDouble', 'assignFloat',	 # int x = 10;
		'assign', 'singleAssign','assignArray','multiAssign',	# x = x + 1;

		'openCurlyBracket', 'closeCurlyBracket',
		'openBoxBracket', 'closeBoxBracket',
		'openCurveBracket', 'closeCurveBracket',

		'print'
	]

	t_singleComm = r'//.+\n'
	t_multCommOpen = r'/\*'
	t_multCommClose = r'\*/'
	t_multComm = t_multCommOpen + r'(.+\n)*' + t_multCommClose

	t_plus = r'\+'
	t_minus = r'-'
	t_times = r'\*'
	t_div = r'/'
	t_num = r'\ *\d+\ *'
	t_bigger = r'>'
	t_smaller = r'<'

	t_newline = r'\n'
	t_equals = r'\ *=\ *'
	t_endline = r';'
	t_comma = r'\ *,\ *'

	t_openCurlyBracket = r'\{'
	t_closeCurlyBracket = r'\}'

	t_openCurveBracket = r'\('
	t_closeCurveBracket = r'\)'
	t_args = t_openCurveBracket + r'(\w+,?)+' + t_closeCurveBracket

	t_openBoxBracket = r'\ *\[\ *'
	t_closeBoxBracket = r'\ *\]\ *'

	t_var = r'\ *[a-zA-Z]\w*\ *(' + t_openBoxBracket + r'(\ *[a-zA-Z]\w*\ *|' + t_num + r')' + t_closeBoxBracket + r')?'

	t_declareInt = r'int\ *' + t_var + t_endline
	t_declareDouble = r'double\ *' + t_var + t_endline
	t_declareFloat = r'float\ *' + t_var + t_endline

	t_assign =   t_var + t_equals + t_minus + r'?\ *(' + t_var + r'|' + t_num + r')\ *([+\-*/]?(' + t_var + r'|' + t_num + r'))*'



	t_assignArray = t_var + t_equals  + t_openCurlyBracket + r'(' + t_num + t_comma + r')*' + t_num + t_closeCurlyBracket

	t_assignInt = r'int\ *' + t_assign
	t_assignDouble = r'double\ *' + t_assign
	t_assignFloat = r'float\ *' + t_assign

	t_singleAssign = r'(' + t_assignInt + r'|' + t_assignFloat + r'|' + t_assignDouble + r'|' + t_assign + r')' + t_endline

	t_multiAssign = r'((' + t_singleAssign + r'|' + t_assignArray + r'|' + t_assignInt + r'|' + t_assignDouble + r'|' + t_assignFloat + r')' + t_comma + r')*' + r'(' + t_singleAssign + r'|' + t_assignArray + r')' + t_endline

	t_callFunc = t_var + t_args
	t_declareFunc = r'function\ *' + t_callFunc
	t_prog = r'program\ *' + t_var
	t_print = r'print\ *' + t_openCurveBracket + r'((' + t_callFunc + r',?)+|(' + t_var + r',?)+)+' + t_closeCurveBracket + t_endline

	t_in = r'\ *in\ *'
	t_to = r'\ *\.\.\ *'
	t_for = r'for\ *' + t_var + t_in + t_openBoxBracket + t_num + t_to + t_num + t_closeBoxBracket
	t_while = r'while\ *' + t_var + r'[' + t_bigger + t_smaller + t_equals + r']' + r'(' + t_var + r'|' + t_num + r')'
	t_if = r'if\ *' + t_var + r'[' + t_bigger + t_smaller + t_equals + r']' + r'(' + t_var + r'|' + t_num + r')'

	t_ignore = r' \n\t'

	lexer = lex.lex()

	if __name__ == "__main__":
		n_teste = input("Teste numero:")
		pwd = "teste" + n_teste + ".txt"
		comentario = False
		with open(pwd, 'r') as file:
			lines = file.readlines()
			print(len(lines))
			for line in lines:
				lexer.input(line)
				for token in lexer:
					if token.type == "multCommOpen":
						comentario = True
					if token.type == "multCommClose":
						comentario = False
					if token.type not in ["newline", "space", "singleComm", "multCommClose"] and not comentario:
						print(f"TIPO: {token.type:<18} | VALOR: {token.value:<10}")
