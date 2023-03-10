#  (?<=er1)er quando tiver er1 antes
#  (?<!er1) er quando nao tiver er1 antes
# exemplo: palavras acabadas em mente ->  (?<=[a-z]+)mente
import sys
import re
import json
import unidecode

def toJson(text):
	listDicionarios = []
	#  comecar por obter uma "template" do dicionario que vai ser usado em cada linha
	splitParams = re.compile(r'([^,]+)[,\n]')
	paramList = re.findall(splitParams, text[0])
	
	
	#encher uma copia do dicionario por linha
	
	for i in range(1, len(text)):
		matches = re.findall(splitParams, text[i])
		matches = [unidecode.unidecode(m) for m in matches]

		if len(matches) == len(paramList):
			dictLine = dict(zip(paramList, matches))
			print(json.dumps(dictLine))


if __name__ == "__main__":
	dir = "teste.csv"
	try:
		with open(dir) as file:
			lines = file.readlines()
		if len(lines) == 0:
			print("Erro, ficheiro vazio")
		else:
			toJson(lines)
		
	except OSError:
		print(f"Ficheiro Invalido -> {dir}")
