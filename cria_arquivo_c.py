VERSAO= "2.0.0"

##função aulixar referente a tradução para a linguagem C

def add_linha(i, var="i", valor="0", ind="0", operacao="+", condicao="i<10"):

    nova_linha = [
        #-----padroes-----
        "#include <stdio.h>\n",                         #id0
        "int main() {\n",                               #id1
        "  return 0;}\n",                               #id2
        #-----definições-----
        "#define True 1",                             #id3
        "#define False 0",                            #id4
        #-----variaveis------
        "float "+ var+";\n",                             #id5
        "float "+ var+"="+ valor+";\n",                  #id6
        "char" + var+"["+ind+"];\n",                     #id7
        "char" + var+"[]"+ "'"+valor+"';\n",             #id8
        "int "+ var+";\n",                      #bool    id9
        "int "+ var+"= True ;\n",               #bool    id10
        "int "+ var+"= False ;\n",              #bool    id11
        #------operações--------
        operacao+ var,                                  #id12        
        operacao+ valor,                                #id13
        "(",                                            #id14
        ")",                                            #id15
        #------funcionalidades-------
        "if("+ condicao +"){\n",                        #id16
        "else{\n",                                      #id17
        "while("+ condicao +"){\n",                     #id18
        "}\n",                                          #id19
        "",                                             #id20
    ]

    return nova_linha[i]



## função referente a criação de arquivo.c apartir das leituras feitas pelo
## interpretador sintatico e semantico do visualAlg

def add_arquivo_c(resultado_sintatico):


    for posicao in range(len(resultado_sintatico)):

        linha = []

        if resultado_sintatico[posicao][0] == 'algoritmo':

            linha.append(add_linha(0))
            linha.append(add_linha(3))
            linha.append(add_linha(4))
            linha.append(add_linha(20))

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'var':

           

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'inicio':

            linha.append(add_linha(1))

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")


        elif resultado_sintatico[posicao][0] == 'fimalgoritmo':

            linha.append(add_linha(2)) 

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

nome_arquivo = "arquivo.c"

with open(nome_arquivo, "w") as arquivo:
    arquivo.write("")

res=[
    ['algoritmo', 'algoritmo'],
    ['var', 'var'],
    ['inicio', 'inicio'],
    ['fimalgoritmo', 'fimalgoritmo']
    ]
var="a"
valor = "2"


add_arquivo_c(res)

