#  (?<=er1)er quando tiver er1 antes
#  (?<!er1) er quando nao tiver er1 antes
# exemplo: palavras acabadas em mente ->  (?<=[a-z]+)mente
import sys
import re
import json
import unidecode

def toJson(text,file_name):
	output = file_name + ".json"
	file = open(output, "w")
	#  comecar por obter uma "template" do dicionario que vai ser usado em cada linha
	splitParams = re.compile(r'([^,\d{}\n]+({\d+,\d+})?)')
	paramList = re.findall(splitParams, text[0])
	
	for i in range(len(paramList)):
		print(paramList[i])
		paramList[i] = paramList[i][0]
		isList = re.match(r'.+{(\d+),(\d+)}', paramList[i])
		if isList:
			paramList[i] = (isList[0].split('{')[0], isList[1], isList[2])
	
	for e in paramList:
		print(type(e))
			
	#encher uma copia do dicionario por linha
	file.write('[\n')
	for i in range(1, len(text)):
		
		matches = re.findall(splitParams, text[i])
		print(matches)
		# matches = [unidecode.unidecode(m) for m in matches]
		if len(matches) == len(paramList) + 1000:
			dictLine = dict(zip(paramList, matches))
			if i == len(matches):
				file.write('\t' + json.dumps(dictLine).replace(',',',\n\t') + '\n')
			else:
				file.write('\t' + json.dumps(dictLine).replace(',',',\n\t') + ',\n')
	file.write(']\n')
	file.close()
	
	
	
if __name__ == "__main__":
	dir = "teste.csv"
	try:
		with open(dir) as file:
			lines = file.readlines()
		if len(lines) == 0:
			print("Erro, ficheiro vazio")
		else:
			toJson(lines, re.search(r'(.+)\.', dir).groups()[0])
		
	except OSError:
		print(f"Ficheiro Invalido -> {dir}")
