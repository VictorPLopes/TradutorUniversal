em_leia = False # variavel que indica se esta dentro de um leia
em_escreva = False # variavel que indica se esta dentro de um escreva
em_para = False # variavel que indica se esta dentro de um para
em_var = False # variavel que indica se esta dentro de um var
em_atrib = False # variavel que indica se esta dentro de um atribuicao

nivel_indentacao = 0 # variavel que indica o nivel de indentacao atual

para_atual = [] # lista que armazena os dados do para atual

# Dicionário para tradução de casos onde a tradução é direta, ou seja, a estrutura é a mesma em C e em VisuAlg
dicionario_traducao_direta = {
    "algoritmo":"""
#include <stdio.h>

#define TRUE 1
#define FALSE 0

""",
    "inicio": "int main() {\n",
    "=": "=",
    "(":"(",
    ")":")",
    ">":">",
    "<":"<",
    ">=":">=",
    "<=":"<=",
    "==":"==",
    "<>":"!=",
    "se":"if",
    "entao": "{\n",
    "senao": "} else {\n",
    "fimse": "}",
    "verdadeiro": "TRUE",
    "falso": "FALSE",
    "faca": "{\n",
    "fimpara": "}",
    "enquanto": "while",
    "fimenquanto": "}",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "e": "&&",
    "ou": "||",
    "fimalgoritmo": "return 0;\n}",
    "inteiro": "int",
    "real": "float",
    "logico": "int"
}

dicionario_scanf_printf = {
    "inteiro": f"%d",
    "real": f"%f",
    "caractere": f"%s"
}

def get_indentacao():
    global nivel_indentacao
    return "    " * nivel_indentacao

# Função que traduz o código de VisuAlg para C
def tradutor(tabela_classificacao, tabela_variavies):
    # Variáveis globais
    global em_leia, em_escreva, em_para, em_var, em_caractere, em_atrib, nivel_indentacao
    
    # Variável que armazena o código traduzido
    codigo = ""
    
    # Para cada palavra na tabela de classificação
    for palavra in tabela_classificacao:
        # Se estiver na parte de declaração de variáveis
        if em_var:
            # Se chegar no fim da declaração de variáveis
            if palavra[0] == "inicio":
                em_var = False
                codigo += dicionario_traducao_direta[palavra[0]]
                nivel_indentacao += 1
                continue
            # Se estiver declarando uma variável
            if palavra[1] == "var":
                # Se for do tipo caractere
                if tabela_variavies[palavra[0]] == "caractere":
                    codigo += "char " + palavra[0] + "[50];\n"
                    continue
                # Se for do tipo inteiro, real ou lógico
                codigo += tabela_variavies[palavra[0]] + palavra[0] + ";\n"
                continue
        
        # Se for uma palavra de tradução direta
        if palavra[0] in dicionario_traducao_direta:
            # Checa se for atribuição
            if palavra[0] == "=":
                em_atrib = True
            # Checa se está no faça de um para
            if palavra[0] == "faca":
                nivel_indentacao += 1
                codigo += para_atual[0] + " = " + para_atual[1] + "; " + para_atual[0] + " <= " + para_atual[2] + "; " + para_atual[0] + "++)"
                # Limpa a lista do para atual
                para_atual.clear()
            # Checa se for um se, enquanto ou senão
            if palavra[0] == "se" or palavra[0] == "enquanto" or palavra[0] == "senao":
                nivel_indentacao += 1
            # Checa se for um fimse, fimenquanto, fimpara ou fimalgoritmo
            if palavra[0] == "fimse" or palavra[0] == "fimenquanto" or palavra[0] == "fimpara" or palavra[0] == "fimalgoritmo":
                nivel_indentacao -= 1
            codigo += dicionario_traducao_direta[palavra[0]]
            # Checa se está em atribuição
            if em_atrib and palavra[0] == ")":
                codigo += ";\n"
                em_atrib = False
            continue
        
        # Senão, se for a parte de declaração de variáveis
        if palavra[0] == "var":
            em_var = True
            continue
        # Senão, se for o nome de uma variável
        if palavra[1] == "var":
            # Se estiver em um leia
            if em_leia:
                codigo += dicionario_scanf_printf[tabela_variavies[palavra[0]]] + ", &" + palavra[0] + ");\n"
                em_leia = False
                continue
            # Se estiver em um escreva
            if em_escreva:
                codigo += dicionario_scanf_printf[tabela_variavies[palavra[0]]] + ", " + palavra[0] + ");\n"
                em_escreva = False
                continue
            # Se estiver em um para
            if em_para:
                para_atual.append(palavra[0])
                continue
            codigo += palavra[0]
            continue
        # Senão, se for uma mensagem (string)
        if palavra[1] == "msg":
            codigo += palavra[0]
            continue
        # Senão, se for um leia
        if palavra[0] == "leia":
            em_leia = True
            codigo += get_indentacao() + "scanf("
            continue
        # Senão, se for um escreva
        if palavra[0] == "escreva":
            em_escreva = True
            codigo += get_indentacao() + "printf("
            continue
        # Senão, se for um para
        if palavra[0] == "para":
            em_para = True
            codigo += get_indentacao() + "for("
            continue
        # Senão, se for um valor inteiro
        if palavra[1] == "inteiro":
            # Se estiver em um para
            if em_para:
                para_atual.append(palavra[0])
                continue
    
    # Retorna o código traduzido
    return codigo