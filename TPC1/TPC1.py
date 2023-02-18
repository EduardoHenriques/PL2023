import math
import pprint


def ler_ficheiro():
    with open("myheart.csv") as file:
        file.readline()                 # a primeira linha nao conta para nada
        linhas = file.readlines()
        return linhas


def filtro(linhas):
    doentes = []
    for l in linhas:
        info = l.split(",")
        if info[5] == "1\n":
            doentes.append(l)
    print(f"Existem {len(doentes)} doentes em {len(linhas)} pacientes,"
          f" ou seja {round( ((len(doentes)/len(linhas))*100),2)}% estão doentes.\n")
    return doentes


def doenca_sexo(linhas):
    doentesF = 0
    doentesM = 0
    res = dict()

    for l in linhas:
        info = l.split(",")
        sexo = info[1]
        if sexo == "M":
            doentesM += 1
        else:
            doentesF += 1

    res["M"] = doentesM
    res["F"] = doentesF
    return res


def doenca_escaloes(linhas):
    res = dict()

    for l in linhas:
        info = l.split(",")
        idade = int(info[0])
        escalao_tipo = math.floor((idade-30)/4)                 # 30 -> 0, 34 -> 1, 38 -> 2, etc
        escalao = f"[{30 + 4 * escalao_tipo},{(30 + 4 * escalao_tipo) + 4}]"
        if escalao in res:
            res[escalao]+=1
        else:
            res[escalao] = 1

    return res

def doenca_colestrol(linhas): # escalao minimo [110-120]
    res = dict()
    for l in linhas:
        info = l.split(",")
        colestrol = int(info[3])
        if colestrol is not 0:
            colestrol_esc = math.floor((colestrol-110)/10)                  # 110 a 120 -> 0, 120 a 130 -> 1
            colestrol_esc = f"[{110 + colestrol_esc * 10},{110 +(colestrol_esc * 10) + 10}]"
            if colestrol_esc in res:
                res[colestrol_esc] +=1
            else:
                res[colestrol_esc] = 1
    return res

#headers -> tupulo(parametro,quantidade)
def to_table(headers,dicionario):
    str_res =      f"{headers[0]}      {headers[1]}\n"
    for para,n in dicionario.items():
        str_res += f"{para}    |  {n}\n"
    print(str_res)



if __name__ == "__main__":
    vals = filtro(ler_ficheiro())
    resultado_dist1 = doenca_sexo(vals)
    resultado_dist2 = doenca_escaloes(vals)
    resultado_dist3 = doenca_colestrol(vals)

    to_table( ("Sexo","Nº"), resultado_dist1 )
    to_table( ("Escalao","Nº"), resultado_dist2 )
    to_table( ("Colestrol","Nº"), resultado_dist3 )

