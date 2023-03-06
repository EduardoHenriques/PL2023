import json
import re
import pprint
import math
import sys
import statistics
from statistics import mode
from statistics import multimode
import collections
# abc… 	Letters
#	123… 	Digits
#	\d 	Any Digit
#	\D 	Any Non-digit character
#	. 	Any Character
#	\. 	Period
#	[abc] 	Only a, b, or c
#	[^abc] 	Not a, b, nor c
#	[a-z] 	Characters a to z
#	[0-9] 	Numbers 0 to 9
#	\w 	Any Alphanumeric character
#	\W 	Any Non-alphanumeric character
#	{m} 	m Repetitions
#	{m,n} 	m to n Repetitions
#	* 	Zero or more repetitions
#	+ 	One or more repetitions
#	? 	Optional character
#	\s 	Any Whitespace
#	\S 	Any Non-whitespace character
#	^…$ 	Starts and ends
#	(…) 	Capture Group
#	(a(bc)) 	Capture Sub-group
#	(.*) 	Capture all
#	(abc|def) 	Matches abc or def
# Dentro dos [] os caracteres especiais perdem o efeito

def datas(txt):
	regexDatas = re.compile(r'([0-9]+)-[0-9]+-[0-9]')  # ::ANO-MES-DIA::
	res = dict()
	for line in txt:
		matches = re.findall(regexDatas,line)
		for match in matches:
			if match in res.keys():
				res[match] += 1
			else:
				res[match] = 1
	return res


def list_to_dict(list):
	res = dict()
	for elem in list:
		if elem in res.keys():
			res[elem] += 1
		else:
			res[elem] = 1
	return res


def nomes(txt):
	resProprios = dict()
	resApelidos = dict()

	regProprio = re.compile(r'::([a-zA-Z]+) ')
	regApelido = re.compile(r'([a-zA-Z]+)::')
	regAno = re.compile(r'::(\d+)-\d+-\d+')

	apelidosTotais = []
	nomesPropriosTotais = []

	for line in txt:
		nomesProprios = re.findall(regProprio,line)
		Apelidos = re.findall(regApelido, line)
		Ano = re.findall(regAno, line)

		if  len(Ano) > 0:
			seculo = math.floor(int(Ano[0])/100) + 1
			seculo = "Século " + str(seculo)
			if seculo not in resProprios.keys():
				resProprios[seculo] = []
			else:
				resProprios[seculo] += nomesProprios
			nomesPropriosTotais += nomesProprios
			if seculo not in resApelidos.keys():
				resApelidos[seculo] = []
			else:
				resApelidos[seculo] += Apelidos
			apelidosTotais += Apelidos


	counterNP = collections.Counter(nomesPropriosTotais)
	counterA = collections.Counter(apelidosTotais)
	most_common_NP = counterNP.most_common(5)
	most_common_A = counterA.most_common(5)

	for key in resProprios:
		resProprios[key] = list_to_dict(resProprios[key])
		#print(resProprios)
	for key in resApelidos:
		resApelidos[key] = list_to_dict(resApelidos[key])
	return (resProprios,resApelidos,most_common_NP,most_common_A)


def familiares(text):
	dict_idades = dict()
	blacklist = ['fls','doc']
	regFamiliares = re.compile(r',([A-Z][a-zA-Z ]+)\.')
	for line in text:
		familiares = re.findall(regFamiliares,line)
		for elem in familiares:
			if elem not in blacklist and not elem.startswith("Sao") and not elem.startswith("Sant"):
				if elem in dict_idades.keys():
					dict_idades[elem] += 1
				else:
					dict_idades[elem] = 1


	return dict_idades


def toJSON(text):
	regexJSON = re.compile(r'(\d+)::(\d+)-(\d+)-(\d+)::([a-zA-Z ]+)::([a-zA-Z ]+)::([a-zA-Z ]+)::(.*)::+')
	for line in text:
		match = re.search(regexJSON,line)
		if match != None:
			dictJSON = dict()
			dictJSON["pid"] = match.groups()[0]
			dictJSON["year"] = match.groups()[1]
			dictJSON["month"] = match.groups()[2]
			dictJSON["day"] = match.groups()[3]
			dictJSON["name"] = match.groups()[4]
			dictJSON["father"] = match.groups()[5]
			dictJSON["mother"] = match.groups()[6]
			dictJSON["other"] = match.groups()[7]
			print(json.dumps(dictJSON))
	return

def print_menu():
    print("Digite a opcao:\n"
         "1->Datas\n"
         "2->Distribuicao de Nomes proprios por seculo + nomes/apelidos mais comuns\n"
         "3->Distribuicao de Apelidos por seculo + nomes/apelidos mais comuns\n"
         "4->Distribuicao Familiares\n"
         "5->ToJSON\n"
         "0->Sair\n")



if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=4)
	with open("processos.txt") as file:
		text = file.readlines()
		resNomes = nomes(text)
		print_menu()
		for opcao in sys.stdin:
			opcao = int(opcao)
			if opcao == 1:
				pp.pprint(datas(text))
				print_menu()
			if opcao == 2:
				for key in resNomes[0]:
					print(f"NOMES PROPRIOS {key}")
					print(f"{resNomes[0][key]}||")

				#for key in resNomes[1]:
				#	print(f"APELIDOS {key}")
				#	pp.pprint(resNomes[1][key])

				print(f"NOMES PROPRIOS MAIS COMUNS:{resNomes[2]}")
				print(F"APELIDOS MAIS COMUNS:{resNomes[3]}")
				print_menu()
			if opcao == 3:
				for key in resNomes[1]:
					print(f"APELIDOS {key}")
					print(f"{resNomes[1][key]}||")

				print(f"NOMES PROPRIOS MAIS COMUNS:{resNomes[2]}")
				print(F"APELIDOS MAIS COMUNS:{resNomes[3]}")
				print_menu()
			if opcao == 4:
				pp.pprint((familiares(text)))
				print_menu()
			if opcao == 5:
				toJSON(text[0:20])
				print_menu()
			if opcao == 0:
				break

