import re
import pprint
#abc… 	Letters
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
#Dentro dos [] os caracteres especiais perdem o efeito

def datas(txt):
	regexDatas = re.compile(r'([0-9]+)-[0-9]+-[0-9]')  # ::ANO-MES-DIA::
	res = dict()
	matches = re.findall(regexDatas,txt)
	for match in matches:
		if match in res.keys():
			res[match] += 1
		else:
			res[match] = 1
	return res


if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=4)
	with open("processos.txt") as file:
		text = file.read()
	dict_datas = datas(text)
	pp.pprint(dict_datas)