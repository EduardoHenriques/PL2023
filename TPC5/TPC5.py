import ply.lex as lex
import sys
import re

list_coinC = ['50', '20', '10', '5']
list_coinE = ['2', '1']


filterMoedas = re.compile(r'(\d{1,2})([ce])')  # ESTA A FUNCIONAR
filterChamadaIN = re.compile(r'00([0-9]{2,3})([0-9]{9})')  # 00[CODIGO][NUMERO-9dig]
filterChamada = re.compile(r'([0-9]{3})([0-9]{6})')  # [NUMERO-3dig][NUMERO-6dig]


def t_error(t):
	print("Caracter ilegal: ", t)
	t.lexer.skip(1)


def parse_moedas(l):
	cent = 0
	eur = 0

	res = filterMoedas.findall(l)
	for coin in res:
		tipo = coin[1]
		val = coin[0]
		if tipo == 'c':
			if val in list_coinC:
				cent += int(coin[0])
			else:
				print(f"moeda inválida:{coin}")

		if tipo == 'e':
			if val in list_coinE:
				eur += int(coin[0])
			else:
				print(f"moeda inválida:{coin}")

	if cent >= 100:
		eur += int(cent / 100)
		cent = cent % 100

	return [eur, cent]


def calcular_saldo(curr, cost):
	total_c = 100 * cost  # transformar  custo em centimos
	total_d = 100 * curr[0] + curr[1]  # transformar saldo  em centimos

	total_d = total_d - total_c  # fazer a conta
	if total_d < 0:
		print("Chamada nao foi executada, nao tem saldo suficiente. Por favor introduza mais moedas...")
		return dinheiro
	else:
		dinheiro[0] = int(total_d / 100)  # atribuir o novo valor ao saldo atual(euros)
		dinheiro[1] = int(total_d % 100)  # atribuir o novo valor ao saldo atual(centimos
		print("Chamada efetuada.")
		return dinheiro


def troco(resto):
	restoE = resto[0]
	restoC = resto[1]
	res = 'O seu troco: '

	for coin in list_coinE:
		count = int(restoE / int(coin))
		if count > 0:
			restoE = restoE - count * int(coin)
			res += (str(count) + ' x ' + coin + ' euro(s), ')

	for coin in list_coinC:
		count = int(restoC / int(coin))
		if count > 0:
			restoC = restoC - count * int(coin)
			res += (str(count) + ' x ' + coin + ' centimos, ')

	res = res[:-2] + '.'
	return res


def parse_numeros(num):
	res = filterChamadaIN.search(num)
	if res:
		print(f"----CHAMADA INTERNACIONAL----\nCodigo: {res.group(1)}\nNumero: {res.group(2)}\nCusto: 1 euro e 50 centimos\n----")

		return 1.5

	res = filterChamada.search(num)
	if res:
		if res.group(1)[0] == '2':
			print("----CHAMADA NACIONAL----\nCusto: 25 centimos\n----")
			return 0.25
		elif res.group(1) == '601' or res.group(1) == '641':
			print("----CHAMADA BLOQUADA----\nCusto: 0\nPor favor, marque outro numero\n----")
			return -1
		elif res.group(1) == '800':
			print("----CHAMADA VERDE----\nCusto: 0\n----")
			return 0
		elif res.group(1) == '808':
			print("----CHAMADA AZUL----\nCusto: 10 centimos\n----")
			return 0.10
		else:
			print("Numero nao reconhecida.")
			return -1
	else:
		print("Numero invalido")
		return 0


if __name__ == "__main__":

	tokens = [
		'moedas',  # sequencia de moedas seguidas de 'MOEDA '
		'digito',  # 0-9
		'coin',  # uma moeda
		'numero',  # T= digitos
		'levantar',  # LEVANTAR\n
		'pousar',  # POUSAR\n
		'newline'  # \n
	]

	t_newline = r'\n'
	t_digito = r'[0-9]'
	t_coin = r'(\ ' + t_digito + r'{1,2}[ce][,.])+'
	t_moedas = r'MOEDA ' + t_coin + t_newline
	t_numero = r'T=\ (' + t_digito + r'+)' + t_newline
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
					print("MÁQUINA JA ESTÁ LIGADA, OPERAÇÃO INVÁLIDA")
				else:
					ligada = True
					print("MAQUINA LIGADA, DEPOSITE MOEDAS:")
			if token.type == 'moedas':
				if ligada:
					saldoLine = parse_moedas(token.value)
					dinheiro[0] += saldoLine[0]
					dinheiro[1] += saldoLine[1]
					print(f"Tem {dinheiro[0]} euro(s) e {dinheiro[1]} centimos de saldo.")
				else:
					print("MAQUINA DESLIGADA, OPERAÇÃO INVALIDA")

			if token.type == 'numero':
				if ligada:
					custo = parse_numeros(token.value)
					if custo >= 0:
						dinheiro = calcular_saldo(dinheiro, custo)
					print(f"Tem {dinheiro[0]} euros e {dinheiro[1]} centimos de saldo.")
				else:
					print("MAQUINA DESLIGADA, OPERAÇÃO INVÁLIDA")
			if token.type == 'pousar':
				if not ligada:
					print("MAQUINA JA ESTAVA DESLIGADA OPERAÇÃO INVALIDA")
				else:
					print(troco(dinheiro)+"\nVolte sempre!")
					exit()
