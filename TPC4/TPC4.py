#  (?<=er1)er quando tiver er1 antes
#  (?<!er1) er quando nao tiver er1 antes
# exemplo: palavras acabadas em mente ->  (?<=[a-z]+)mente
import re
import json
import unidecode
import subprocess


def dictToLine(dic, lastLineFlag):
	if len(dic) > 1:
		res = json.dumps(dic) + ',\n' if not lastLineFlag else json.dumps(dic) + '\n'
		res = re.sub(r', ', r',\n\t', res)
		res = re.sub(r']}\n', r']\n\t}', res)
		res = re.sub(r']},\n', r']\n\t},\n', res)
		res = re.sub(r': \[', r':\n\t[', res)
		return res
	else:
		return "\n"


def decode(lista):
	for i in range(len(lista)):
		if isinstance(lista[i], str):
			lista[i] = unidecode.unidecode(lista[i])
	return lista


def transform_list(lst, start_idx, end_idx):
	if end_idx > len(lst):
		end_idx = len(lst)
	else:
		pass
	return lst[:start_idx] + [lst[start_idx:end_idx+1]] + lst[end_idx+1:]


def toJson(text, file_name):
	output = file_name + '.json'
	file = open(output, "w")
	splitParams = re.compile(r'([^,\d{}\n]+({\d+,\d+})?)')  	# expressao regular que encontra os campos a analisar
	splitLine = re.compile(r'[^,\n ]+[,\n]')				# expressao regular que encontra os valores nas linhas
	isList = re.compile(r'[a-zA-Z]+{(\d+),(\d+)}')			# expressao regular que encontra os limites no param s{n,m}

	#  comecar por obter uma "template" do dicionario que vai ser usado em cada linha
	paramList = re.findall(splitParams, text[0])
	
	for i in range(len(paramList)):
		paramList[i] = paramList[i][0]

	# encher uma copia do dicionario por linha
	file.write('[\n')
	for i in range(1, len(text)):	 # parse a uma linha
		matches = re.findall(splitLine, text[i])
		for j in range(len(paramList)):	 	# passa por cada parametro
			if re.match(isList, paramList[j]):	 	# parametro é do tipo str{n,m} ?
				n = (re.match(isList, paramList[j]).groups()[0])  	# n
				m = (re.match(isList, paramList[j]).groups()[1])  	# m
				matches = decode(transform_list(matches, j+int(n)-1, j+int(m)-1))

		dictLine = dict(zip(paramList, matches))  	# funcao que transforma um dicionario numa string formato JSON
		if i == len(text)-2:
			l = '\t' + dictToLine(dictLine, True)
		else:
			l = '\t' + dictToLine(dictLine, False)
		file.write(l)
	file.write(']\n')
	file.close()
	print(f'Ficheiro {file_name}.csv convertido para {file_name} json')


if __name__ == "__main__":

	print("FICHEROS NA DIRETORIA:\n--------------\n")
	subprocess.run(["ls"])
	print("\n--------------\nDigite o nome do ficheiro para converter(.csv)")
	csvdir = input()
	try:
		with open(csvdir) as csvfile:
			lines = csvfile.readlines()
		if len(lines) == 0:
			print("Erro, ficheiro vazio")
		else:
			toJson(lines, re.search(r'(.+)\.', csvdir).groups()[0])
		
	except OSError:
		print(f"Ficheiro Invalido -> {csvdir}")
