em_var = False # variavel que indica se esta dentro de um var
em_atrib = False # variavel que indica se esta dentro de um atribuicao

nivel_indentacao = 0 # variavel que indica o nivel de indentacao atual

dic_tipos = {"inteiro": "int", "real": "float", "caractere": "char", "logico": "int"}

dic_strings = {"inteiro": f"%d", "real": f"%f", "caractere": f"%s", "logico": f"%d"}

def get_indentacao():
    global nivel_indentacao
    return "    " * nivel_indentacao

# Função que traduz o código de VisuAlg para C
def tradutor(tabela_de_classificação, tabela_variavies):
    # Variáveis globais
    global em_var, em_atrib, nivel_indentacao
    
    # Variável que armazena o código traduzido
    codigo = ""
    
    i = 0 # Variável que armazena o índice da tabela de classificação
    
    # Para cada palavra na tabela de classificação
    while i < (len(tabela_de_classificação)):
        # Se a palavra for algoritmo
        if tabela_de_classificação[i][1] == "algoritmo":
            codigo += "#include <stdio.h>\n#include <string.h>\n\n#define TRUE 1\n#define FALSE 0\n\n"
        
        # Se a palavra for var (início da seção de declaracao de variáveis)
        elif tabela_de_classificação[i][0] == "var":
            em_var = True
        
        # Se for uma variável
        elif tabela_de_classificação[i][1] == "var":
            # Se estiver dentro da seção de declaração de variáveis
            if em_var:
                # Se for do tipo caractere
                if tabela_de_classificação[i+1][1] == "caractere":
                    codigo += dic_tipos[tabela_de_classificação[i+1][1]] + " " + tabela_de_classificação[i][0] + "[100];\n"
                else:
                    codigo += dic_tipos[tabela_de_classificação[i+1][1]] + " " + tabela_de_classificação[i][0] + ";\n"
                i += 2 # Pula o tipo da variável
                continue
            # Se não estiver dentro da seção de declaração de variáveis
            # Se for uma atribuição
            elif tabela_de_classificação[i+1][0] == "=":
                # Se for uma string (mensagem), ignora, pois um strcpy será feito depois ao ler a mensagem
                if tabela_variavies[tabela_de_classificação[i][0]] == "caractere":
                    i += 2 # Pula =
                    em_atrib = True
                    continue
                codigo += get_indentacao()
            codigo += tabela_de_classificação[i][0] + " "
            # Se tiver finalizado uma atribuição
            if em_atrib and tabela_de_classificação[i+1][0] not in ["e", "ou", ")", ">=", "<=", ">", "<", "+", "-", "*", "/", "==", "<>"]:
                codigo += ";\n"
                em_atrib = False
        
        # Se for inicio
        elif tabela_de_classificação[i][0] == "inicio":
            codigo += "\nint main() {\n"
            nivel_indentacao += 1
            em_var = False
        
        # Se for leia
        elif tabela_de_classificação[i][0] == "leia":
            codigo += get_indentacao() + "scanf(\"" + dic_strings[tabela_variavies[tabela_de_classificação[i+2][0]]] + "\", &" + tabela_de_classificação[i+2][0] + ");\n"
            i += 4 # Pula (, variavel, )
            continue
        
        # Se for escreva
        elif tabela_de_classificação[i][0] == "escreva":
            # Se for uma string (mensagem)
            if tabela_de_classificação[i+2][1] == "msg":
                codigo += get_indentacao() + "printf(" + tabela_de_classificação[i+2][0] + ");\n"
            # Se for uma variável
            else:
                codigo += get_indentacao() + "printf(\"" + dic_strings[tabela_variavies[tabela_de_classificação[i+2][0]]] + "\", " + tabela_de_classificação[i+2][0] + ");\n"
            i += 4 # Pula (, variavel, )
            continue
        
        # Se for um = (atribuição)
        elif tabela_de_classificação[i][0] == "=":
            codigo += "= "
            em_atrib = True
        
        # Se ler um valor, verdadeiro, falso ou )
        elif tabela_de_classificação[i][1] in ["valor", "verdadeiro", "falso", ")"]:
            # Para verdadeiro e falso
            if tabela_de_classificação[i][1] == "verdadeiro":
                codigo += "TRUE "
            elif tabela_de_classificação[i][1] == "falso":
                codigo += "FALSE "
            else:
                codigo += tabela_de_classificação[i][0] + " "
            # Se tiver finalizado uma atribuição
            if em_atrib and tabela_de_classificação[i+1][0] not in ["e", "ou", ")", ">=", "<=", ">", "<", "+", "-", "*", "/", "==", "<>"]:
                codigo += ";\n"
                em_atrib = False
                
        # Se ler uma mensagem
        elif tabela_de_classificação[i][1] == "msg":
            # Se estiver em uma atribuição, realiza strcpy
            if em_atrib:
                codigo += get_indentacao() + "strcpy(" + tabela_de_classificação[i-2][0] + ", " + tabela_de_classificação[i][0] + ");\n"
                em_atrib = False
        
        # Se ler um operador <>
        elif tabela_de_classificação[i][0] == "<>":
            codigo += "!= "
        
        # Se ler um operador e
        elif tabela_de_classificação[i][0] == "e":
            codigo += "&& "
        
        # Se ler um operador ou
        elif tabela_de_classificação[i][0] == "ou":
            codigo += "|| "
        
        # Se ler um operador ==, >=, <=, >, <, +, -, *, / ou um (
        elif tabela_de_classificação[i][0] in ["==", ">=", "<=", ">", "<", "+", "-", "*", "/", "("]:
            codigo += tabela_de_classificação[i][0] + " "
        
        # Se ler um se
        elif tabela_de_classificação[i][0] == "se":
            codigo += get_indentacao() + "if "
        
        # Se ler um entao ou um faca
        elif tabela_de_classificação[i][0] == "entao" or tabela_de_classificação[i][0] == "faca":
            codigo += " {\n"
            nivel_indentacao += 1
        
        # Se ler um senao
        elif tabela_de_classificação[i][0] == "senao":
            nivel_indentacao -= 1
            codigo += get_indentacao() + "} else {\n"
            nivel_indentacao += 1
        
        # Se ler um fimse ou um fimpara ou um fimenquanto
        elif tabela_de_classificação[i][0] in ["fimse", "fimpara", "fimenquanto"]:
            nivel_indentacao -= 1
            codigo += get_indentacao() + "}\n"
        
        # Se ler um para
        elif tabela_de_classificação[i][0] == "para":
            codigo += get_indentacao() + f"for ({tabela_de_classificação[i+1][0]} = {tabela_de_classificação[i+3][0]}; {tabela_de_classificação[i+1][0]} <= {tabela_de_classificação[i+5][0]}; {tabela_de_classificação[i+1][0]}++) "
            i += 6 # Pula variavel, de, valor, ate e valor
            continue
        
        # Se ler um enquanto
        elif tabela_de_classificação[i][0] == "enquanto":
            codigo += get_indentacao() + "while "
        
        # Se ler um fimalgoritmo
        elif tabela_de_classificação[i][0] == "fimalgoritmo":
            codigo += get_indentacao() + "return 0;\n}\n"
        
        # Incrementa o índice
        i += 1
    
    # Retorna o código traduzido
    return codigo