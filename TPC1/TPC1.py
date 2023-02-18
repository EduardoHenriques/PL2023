import math
import matplotlib.pyplot as plt
import sys

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
    res_ints = dict()                                           # dicionario do tipo 0->31,1->35,etc...

    for l in linhas:
        info = l.split(",")
        idade = int(info[0])
        escalao_tipo = math.floor((idade-30)/4)                 # idade 30 -> escalao 0, 34 -> 1, 38 -> 2, etc...
        if escalao_tipo in res_ints:
            res_ints[escalao_tipo] +=1
        else:
            res_ints[escalao_tipo] = 1
    # sorting
    keys_sorted = sorted(res_ints.keys())
    values_sorted = [res_ints[key] for key in keys_sorted]
    res = { f"[{30 + 4 * keys_sorted[i]},{(30 + 4 * keys_sorted[i]) + 4}]" : values_sorted[i] for i in range(len(keys_sorted))}

    return res


def doenca_colestrol(linhas): # escalao minimo [100-110]
    res_ints = dict()
    res_ints[-1] = 0            # -1 significa que tem nao tem colestrol(0). O minimo é 107 nos dados logo qualquer
                                # valor abaixo conta como 0
    for l in linhas:
        info = l.split(",")
        colestrol = int(info[3])
        if colestrol == 0:
            res_ints[-1] += 1
        else:
            colestrol = math.floor((colestrol - 100)/10)
            if colestrol in res_ints:
                res_ints[colestrol] +=1
            else:
                res_ints[colestrol] = 1
    #sorting
    keys_sorted = sorted(res_ints.keys())
    values_sorted = [res_ints[key] for key in keys_sorted]
    res = dict()
    res["0 ou <100"] = values_sorted[0]
    for i in range(1,len(keys_sorted)):
        res[f"[{100 + 10 * keys_sorted[i]},{(100 + 10 * keys_sorted[i]) + 10}]"] = values_sorted[i]

    return res

#headers -> triplo(parametro,quantidade,%)
def to_table(headers,dicionario, total):
    str_res =      f" {headers[0]:<5} || {headers[1]:<7} || {headers[2]:<4}\n---------------------------\n"
    for para,n in dicionario.items():
        perc = round( (n/total * 100), 2)
        str_res += f" {para:<5} || {n:<7}    || {perc:<4} \n"
    print(str_res)
    return

def to_plot(dicionario,legendaX,legendaY,titulo):
    n = dicionario.values()
    parametro = dicionario.keys()
    fig = plt.figure(figsize= (10,5))
    plt.bar(parametro,n, color='blue', width = 0.3)
    plt.xticks(range(len(dicionario)), dicionario.keys(), rotation='vertical')
    plt.ylabel(legendaY)
    plt.title(titulo)
    plt.show()
    return

def print_menu():
    print("Digite a opcao:\n"
         "1->Tabela Distribuição Sexo\n"
         "2->Tabela Distribuição Faixa Etaria\n"
         "3->Tabela Distribuição Colestrol\n"
         "4->Plot Distribuição Sexo\n"
         "5->Plot Distribuição Faixa Etaria\n"
         "6->Plot Distribuição Colestrol\n"
         "0->Sair\n")

if __name__ == "__main__":
    vals = filtro(ler_ficheiro()) # ler o ficheior e filtrar quem não está doente para as distribuicoes
    n_doentes = len(vals)
    resultado_dist1 = doenca_sexo(vals)        #dicionario
    resultado_dist2 = doenca_escaloes(vals)    #dicionario
    resultado_dist3 = doenca_colestrol(vals)   #dicionario

    print_menu()
    for opcao in sys.stdin:
        opcao = int(opcao)
        if opcao == 1:
            to_table(("Sexo", "Nº Doentes", "%"), resultado_dist1, n_doentes)
            print_menu()
        elif opcao == 2:
            to_table(("Escalao", "Nº Doentes", "%"), resultado_dist2, n_doentes)
            print_menu()
        elif opcao == 3:
            to_table(("Colestrol", "Nº Doentes", "%"), resultado_dist3, n_doentes)
            print_menu()
        elif opcao == 4:
            to_plot(resultado_dist1, "Sexo", "Nº Doentes", "Distribuição por sexo")
        elif opcao == 5:
            to_plot(resultado_dist2,"Idade","Nº Doentes","Distribuição por faixas etárias")
        elif opcao == 6:
            to_plot(resultado_dist3, "Colestrol", "Nº Doentes", "Distribuição por nível colestrol")
        else:
            break

