
def add_arquivo_c(resultado_sintático, var, valor, ind):

    nova_linha = [
        "#include <stdio.h>\n",
        "#define True 1\n",
        "#define False 0\n",
        "int main() {\n",
        "  return 0;}\n",
        "float "+ var+";\n",
        "float "+ var+"="+str(valor)+";\n",
        "char" + var+"["+ind+"];\n",
        "char" + var+"[]"+ "'"+valor+"';\n",
        "int "+ var+";\n",                      #bool
        "int "+ var+"= True ;\n",
        "int "+ var+"= False ;\n",
        "",
        "",
        "",
        "",
        
    ]
    nome_arquivo = "arquivo.c"

    linha = nova_linha[4]

    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(linha+"\n")

res=["12345"]
var="a"
valor = "2"
ind= "0"

add_arquivo_c(res, var, valor, ind)

