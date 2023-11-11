 
## função referente a criação de arquivo.c apartir das leituras feitas pelo
## interpretador sintatico e semantico do visualAlg

def add_arquivo_c(resultado_sintático, var, valor, ind=0, operacao="+", condicao="i<10"):

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
        "float "+ var+"="+str(valor)+";\n",
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
        "if("+ +"){",
        "else{",
        "while("+ condicao +"){",
        "for("+  +";"+ condicao +";"+  +"){",
        "}"
        
    ]
    nome_arquivo = "arquivo.c"

    linha = nova_linha[4]

    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(linha+"\n")

res=["12345"]
var="a"
valor = "2"


add_arquivo_c(res, var, valor)

