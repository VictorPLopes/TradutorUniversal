VERSAO= "2.0.1"

##função aulixar referente a tradução para a linguagem C

def add_linha(i, var="i", valor="0", ind="100", operacao="+", condicao="i<10"):

    nova_linha = [
    #-----padroes-----
    "#include <stdio.h>\n",  # id0
    "int main() {\n",       # id1
    "  return 0;\n",        # id2
    #-----definições-----
    "#define True 1\n",     # id3
    "#define False 0\n",    # id4
    #-----variaveis------
    "int " + var + ";\n",                   # id5
    var + " = " + valor + ";\n",            # id6
    "float " + var + ";\n",                 # id7
    var + " = " + valor + ";\n",            # id8
    "char " + var + "[" + ind + "];\n",     # id9
    "char " + var + "[] = '" + valor + "';\n",  # id10
    "int " + var + ";\n",                    # bool id11
    var + " = True;\n",             # bool id12
    var + " = False;\n",            # bool id13
    #------operações--------
    operacao + var + ";\n",      # id14
    operacao + valor + ";\n",    # id15
    "(\n",                       # id16
    ")\n",                       # id17
    #------funcionalidades-------
    "if (" + condicao + ") {\n",        # id18
    "} else {\n",                        # id19
    "while (" + condicao + ") {\n",     # id20
    "for (" + var + " = " + valor + "; " + condicao + "; " + var + "++) {\n",  # id21
    "}\n",                              # id22
    ""                                  # id23
]


    return nova_linha[i]

def condicional(i, var='a', valor="5"):
    cond=[
    var + ">" + var,    #id0
    var + ">" + valor,  #id1
    var + "<" + var,    #id2
    var + "<" + valor,  #id3
    var + ">=" + var,   #id4
    var + ">=" + valor, #id5
    var + "<=" + var,   #id6
    var + "<=" + valor, #id7
    var + "==" + var,   #id8
    var + "==" + valor, #id9
    var + "!=" + var,   #id10
    var + "!=" + valor, #id11
]


    return cond[i]

## função referente a criação de template.c apartir das leituras feitas pelo
## interpretador sintatico e semantico do visualAlg

def add_arquivo_c(resultado_sintatico):
    
    for posicao in range(len(resultado_sintatico)):

        linha = []

        if resultado_sintatico[posicao][0] == 'algoritmo':

            linha.append(add_linha(0))
            linha.append(add_linha(3))
            linha.append(add_linha(4))
            

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'var':

            while(resultado_sintatico[posicao+1][0] != 'inicio'):
                linha.append(add_linha())
                if resultado_sintatico[posicao][0]== "inteiro":
                    linha.append(add_linha(5,resultado_sintatico[posicao][1]))
                elif resultado_sintatico[posicao][0]== "real":
                    linha.append(add_linha(7,resultado_sintatico[posicao][1]))
                elif resultado_sintatico[posicao][0]== "caracter":
                    linha.append(add_linha(9,resultado_sintatico[posicao][1]))
                elif resultado_sintatico[posicao][0]== "logico":
                    linha.append(add_linha(11,resultado_sintatico[posicao][1]))

                prosicao=posicao+1

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

nome_arquivo = "template.c"

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