import ply.lex as lex
import sys
import re


def t_error(t):
	print("Caracter illegal: ", t)
	t.lexer.skip(1)


def parse_moedas(l):
	cent = 0
	eur = 0
	list_coinC = ['5', '10', '20', '50']
	list_coinE = ['1', '2']
	filterMoedas = re.compile(r'(\d{1,2})([ce])')

	res = filterMoedas.findall(l)
	for coin in res:
		tipo = coin[1]
		val = coin[0]
		if tipo == 'c':
			if val in list_coinC:
				cent += int(coin[0])
			else:
				print(f"moeda invalida:{coin}")

		if tipo == 'e':
			if val in list_coinE:
				eur += int(coin[0])
			else:
				print(f"moeda invalida:{coin}")

	if cent >= 100:
		eur += int(cent / 100)
		cent = cent % 100

	return [eur, cent]


	#  WIP
def parse_numeros(num):
	return


if __name__ == "__main__":

	blacklist = ['601', '641']

	tokens = [
		'moedas',
		'digito',
		'coin',
		'depositar',
		'numero',
		'levantar',
		'pousar',
		'newline'
	]

	t_newline = r'\n'
	t_digito = r'[0-9]'
	t_coin = r'(\ ' + t_digito + r'{1,2}[ce][,.])+'
	t_moedas = r'MOEDA ' + t_coin
	t_numero = r'T=' + t_digito + r'{3}' + t_digito + r'{6}' + t_newline
	t_levantar = r'LEVANTAR' + t_newline
	t_pousar = r'POUSAR' + t_newline

	t_ignore = r'^.+$'

	lexer = lex.lex()

	dinheiro = [0, 0]  # E,c
	ligada = False

	for line in sys.stdin:
		lexer.input(line)
		for token in lexer:
			if token.type == 'levantar':
				if ligada:
					print("MAQUINA JA ESTÁ LIGADA, OPERAÇÃO INVÁLIDA")
				else:
					ligada = True
					print("MAQUINA LIGADA, DEPOSITE MOEDAS:")
			if token.type == 'moedas':
				if ligada:
					saldoLine = parse_moedas(token.value)
					dinheiro[0] += saldoLine[0]
					dinheiro[1] += saldoLine[1]
					print(f"Tem {dinheiro[0]} euros e {dinheiro[1]} centimos de saldo.")

			if token.type == 'numero':
				#  parsing dos numeros por fazer
				parse_numeros(token.value)
			if token.type == 'pousar':
				if not ligada:
					print("MAQUINA JA ESTAVA DESLIGADA OPERAÇÃO INVALIDA")
				else:
					print(f"TROCO: {dinheiro[0]} euros e {dinheiro[1]} centimos. Volte sempre!")
