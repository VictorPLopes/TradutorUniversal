VERSAO= "2.0.4"

##----flags-----
WT = 0
RD = 0



##função aulixar referente a tradução para a linguagem C

def add_linha(i, var="i",var_2 = "y", valor="0", ind="100", operacao="+", condicao="i < 10"):

    nova_linha = [
    #-----padroes-----
    "#include <stdio.h>\n",            # id0
    "int main() {\n",                  # id1
    "  return 0;\n",                   # id2
    #-----definicoes-----
    "#define True 1\n",                # id3
    "#define False 0\n",               # id4
     #-----variaveis------
    "int " + var + ";\n",              # id5
    "float " + var + ";\n",            # id6
    "char " + var + "[" + ind + "];\n",# id7
    #------funcionalidades-------
    'scanf"',                          # id8
    '%d", &',                          # id9
    '%f", &',                          # id10
    '%s", ',                           # id11
    '%c", &',                          # id12
    '", &',                            # id13
    'printf',                          # id14
    ','+ var + ');\n',                 # id15
    'if ',                            # id16
    '} else {',                        # id17
    'while',                           # id18
    'for (',                           # id19
    '; '+ var + '++) {\n',             # id20
    '{\n',                             # id21
    '}\n',                             # id22
    ';\n',                             # id23
    ';'                                # id24
]




    return nova_linha[i]

## Lista de condicionais

def condicional(i, var='a', valor="5", express = " x + 1"):
    cond=[
    var + ">" + var,    #id0
    var + ">" + valor,  #id1
    valor + ">" + var,  #id2
    var + "<" + var,    #id3
    var + "<" + valor,  #id4
    valor + "<" + var,  #id5
    var + ">=" + var,   #id6
    var + ">=" + valor, #id7
    valor + ">=" + var, #id8
    var + "<=" + var,   #id9
    var + "<=" + valor, #id10
    valor + "<=" + var, #id11
    var + "==" + var,   #id12
    var + "==" + valor, #id13
    valor + "==" + var, #id14
    var + "!=" + var,   #id15
    var + "!=" + valor, #id16
    valor + "!=" + var, #id17
    "&&",               #id18
    "||"                #id19
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

            if resultado_sintatico[posicao][1] == 'var':

                while(resultado_sintatico[posicao+1][0] != 'inicio'):
                    if resultado_sintatico[posicao][0]== "inteiro" or resultado_sintatico[posicao][0]== "logico":
                        linha.append(add_linha(5,resultado_sintatico[posicao][1]))
                    elif resultado_sintatico[posicao][0]== "real":
                        linha.append(add_linha(6,resultado_sintatico[posicao][1]))
                    elif resultado_sintatico[posicao][0]== "caracter":
                        linha.append(add_linha(7,resultado_sintatico[posicao][1]))

                    prosicao=posicao+1

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'inicio':

            linha.append(add_linha(1))

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'leia':

            RD = 1

            linha.append(add_linha(8))

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'escreve':

            WT = 1

            linha.append(add_linha(14)) 

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'se':

            linha.append(add_linha(16))  

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")
            
        elif resultado_sintatico[posicao][0] == 'senao':

            linha.append(add_linha(17))   

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'entao' or resultado_sintatico[posicao][0] == 'faca':

            linha.append(add_linha(21))     
            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'enquanto':

            linha.append(add_linha(18))    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")
            
        elif resultado_sintatico[posicao][0] == 'para':

            linha.append(add_linha(19))    
            posicao = posicao + 1
            while(resultado_sintatico[posicao+1][0] != 'inicio'):
                
                if resultado_sintatico[posicao][1]== "var":
                    linha.append(resultado_sintatico[posicao][0])
                elif resultado_sintatico[posicao][0]== "de":
                    linha.append("=")
                elif resultado_sintatico[posicao][1]== "valor":
                    linha.append(resultado_sintatico[posicao][0])
                elif resultado_sintatico[posicao][0]== "ate":
                    linha.append(";" + resultado_sintatico[posicao-3][0] + "<")
                elif resultado_sintatico[posicao][0]== "faca":
                    linha.append(";" + resultado_sintatico[posicao-5][0] + "++ ) {")

                posicao = posicao + 1

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")
        
        elif resultado_sintatico[posicao][0] == 'fimenquanto' or resultado_sintatico[posicao][0] == 'fimpara' or resultado_sintatico[posicao][0] == 'fimse':
            
            linha.append(add_linha(22))

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'fimalgoritmo':

            linha.append(add_linha(2)) 

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '(':

            linha.append("(")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == ')':

            linha.append(")")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '>':

            linha.append(">")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '<':

            linha.append("<")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '==':

            linha.append("==")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '=':

            linha.append("=")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '<=':

            linha.append("<=")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '>=':

            linha.append(">=")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '<>':

            linha.append("!=")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '+':

            linha.append("+")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '-':

            linha.append("-")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '*':

            linha.append("*")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == '/':

            linha.append("/")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'e':

            linha.append("&&")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")
        
        elif resultado_sintatico[posicao][0] == 'ou':

            linha.append("||")    

            for i in range(len(linha)):
                with open(nome_arquivo, "a") as arquivo:
                    arquivo.write(linha[i]+"\n")

        elif resultado_sintatico[posicao][0] == 'msg':

            linha.append(resultado_sintatico[posicao][0] + ";")    

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