 

def add_linha(i, var="i", valor="0", ind="0", operacao="+", condicao="i<10"):

    nova_linha = [
        #-----padroes-----
        "#include <stdio.h>\n",
        "int main() {\n",
        "  return 0;}\n",
        #-----definições-----
        "#define True 1\n",
        "#define False 0\n",
        #-----variaveis------
        "float "+ var+";\n",
        "float "+ var+"="+ valor+";\n",
        "char" + var+"["+ind+"];\n",
        "char" + var+"[]"+ "'"+valor+"';\n",
        "int "+ var+";\n",                      #bool
        "int "+ var+"= True ;\n",               #bool
        "int "+ var+"= False ;\n",              #bool
        #------operações--------
        operacao+ var,
        operacao+ valor,
        "(",
        ")",
        #------funcionalidades-------
        "if("+ condicao +"){\n",
        "else{\n",
        "while("+ condicao +"){\n",
        "}\n",
        "\n",
    ]

    return nova_linha[i]



## função referente a criação de arquivo.c apartir das leituras feitas pelo
## interpretador sintatico e semantico do visualAlg

def add_arquivo_c(resultado_sintático):

    
    nome_arquivo = "arquivo.c"

    linha = add_linha(1)

    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(linha+"\n")

res=["12345"]
var="a"
valor = "2"


add_arquivo_c(res)

