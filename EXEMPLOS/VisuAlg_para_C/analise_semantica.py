# Definição da analise semântica
def analise_semantica(tabela_de_classificação, debug=False):
    print("\nIniciando análise semântica...\n")
    tabela_variavies = {}  # dicionário vazio
    passa_reto = [ # lista de tokens que podem ser ignorados
        "algoritmo",
        "inteiro",
        "real",
        "caractere",
        "logico",
        "verdadeiro",
        "falso",
        "e",
        "ou",
        "escreva",
        "leia",
        "se",
        "entao",
        "fimse",
        "senao",
        "para",
        "de",
        "ate",
        "faca",
        "fimpara",
        "enquanto",
        "fimenquanto",
        "msg",
        "valor",
        "op_arit",
        "compara",
        "(",
        ")"]

    declara = False # controla a declaração de variáveis

    # vamos percorrer a tabela_de_classificação
    # em busca de ['var','var'] que indica
    # a sessão de declaração de variáveis
    # que termina com ['inicio','inicio']
    # temos que buscar pelo terminal[0] = 'var'
    # e finalizar a busca com o terminal[0] = 'inicio'

    for posicao in range(len(tabela_de_classificação)):
        # Se o debug estiver ativado, imprime o lexema e o token da posição atual
        if debug:
            print(f"Analisando sintaxe de {tabela_de_classificação[posicao]}")
            
        # Se o token da posição atual estiver na lista de tokens que devem ser ignorados, passa para a próxima posição
        if tabela_de_classificação[posicao][1] in passa_reto:
            continue
        
        if tabela_de_classificação[posicao][0] == 'var': # declarações da variáveis
            declara = True # inicia a etapa de declaração de variáveis
            continue # passa para a próxima posição

        elif tabela_de_classificação[posicao][0] == 'inicio':
            declara = False  # finaliza a busca
            if debug:
                print("\nTabela de variáveis:\n", tabela_variavies, "\n")
            continue # passa para a próxima posição
        
        # Quando lê um fimalgoritmo retorna
        elif tabela_de_classificação[posicao][1] == 'fimalgoritmo':
            return True, "Análise semântica concluída com sucesso.", tabela_variavies
        
        # Quando lê uma variável
        elif tabela_de_classificação[posicao][1] == 'var':
            # Se estiver na etapa de declaração de variáveis
            if declara: # se estiver declarando variável
                tabela_variavies[tabela_de_classificação[posicao][0]] = tabela_de_classificação[posicao+1][0] # adiciona a variável e seu tipo na tabela
                posicao += 1 # pula para a próxima posição
                continue # passa para a próxima posição
            # Senão, salva o nome da variável e checa se está na tabela de variáveis
            var = tabela_de_classificação[posicao][0]
            if var in tabela_variavies:
                # Se o tipo da variável for lógico
                if tabela_variavies[var] == 'logico':
                    # Se houver um leia antes, rejeita
                    if tabela_de_classificação[posicao-2][1] == 'leia':
                        return False, f"Variável {var} é do tipo lógico e não pode ser lida."
                    # Se houver um escreva antes, rejeita
                    elif tabela_de_classificação[posicao-2][1] == 'escreva':
                        return False, f"Variável {var} é do tipo lógico e não pode ser escrita."
                    # Se houver um compara antes, testa se está comparando corretamente
                    elif tabela_de_classificação[posicao-1][1] == 'compara':
                        # Para o tipo lógico, só é permitido comparar igualdade ou diferença com outro lógico ou com verdadeiro ou falso
                        if tabela_de_classificação[posicao-1][0] == '==' or tabela_de_classificação[posicao-1][0] == '<>':
                            if (tabela_de_classificação[posicao-2][1] == 'verdadeiro' or tabela_de_classificação[posicao-2][1] == 'falso') or tabela_variavies[tabela_de_classificação[posicao-2][0]] == 'logico':
                                continue
                            else:
                                return False, f"A variável {var} não pode ser comparada com {tabela_de_classificação[posicao-2][0]}. Ela só pode ser comparada com outra variável lógica ou com verdadeiro ou falso."
                        else:
                            return False, f"A variável {var} não pode ser comparada com o operador {tabela_de_classificação[posicao-1][0]}."
                # Se o tipo da variável for numérico
                elif tabela_variavies[var] == 'inteiro' or tabela_variavies[var] == 'real':
                    # Caso especial para o tipo inteiro no comando para
                    if tabela_de_classificação[posicao-1][1] == 'para':
                        if tabela_variavies[var] == 'inteiro':
                            # Testa se o intervalo é válido
                            if tabela_de_classificação[posicao+2][0] < tabela_de_classificação[posicao+4][0]:
                                continue
                            else:
                                return False, f"A variável {var} não pôde ser inicializada com o intervalo especificado, pois o valor inicial {tabela_de_classificação[posicao+2][0]} é maior que o valor final {tabela_de_classificação[posicao+4][0]}."
                        else:
                            return False, f"A variável {var} não pode ser inicializada no comando para, pois não é do tipo inteiro."
                    # Se houver um leia antes, aceita
                    if tabela_de_classificação[posicao-2][1] == 'leia':
                        continue
                    # Se houver um compara antes, testa se está comparando corretamente
                    elif tabela_de_classificação[posicao-1][1] == 'compara':
                        # Para o tipo numérico, é permitido comparar igualdade, diferença, maior, menor, maior ou igual e menor ou igual com outro numérico
                        if tabela_de_classificação[posicao-2][1] == 'valor' or (tabela_variavies[tabela_de_classificação[posicao-2][0]] == 'inteiro' or tabela_variavies[tabela_de_classificação[posicao-2][0]] == 'real'):
                            continue
                        else:
                            return False, f"A variável {var} não pode ser comparada com {tabela_de_classificação[posicao-2][0]}. Ela só pode ser comparada com outra variável numérica ou com um valor."
                # Se o tipo da variável for mensagem
                elif tabela_variavies[var] == 'caractere':
                    # Se houver um leia antes, aceita
                    if tabela_de_classificação[posicao-2][1] == 'leia':
                        continue
                    # Se houver um compara antes, rejeita
                    elif tabela_de_classificação[posicao-1][1] == 'compara':
                        return False, f"A variável {var} é do tipo caractere e não pode ser comparada com {tabela_de_classificação[posicao-2][0]}."
                    
            else:
                return False, f"Variável {var} não declarada."
            
        # Quando lê um operador de atribuição
        elif tabela_de_classificação[posicao][1] == 'atrib':
            # Salva o tipo da variável
            tipo = tabela_variavies[tabela_de_classificação[posicao-1][0]]
            # Se o tipo da variável for lógica
            if tipo == 'logico':
                # Para o tipo lógico, só é permitido atribuir verdadeiro, falso ou outro lógico
                if tabela_de_classificação[posicao+1][1] == 'verdadeiro' or tabela_de_classificação[posicao+1][1] == 'falso' or tabela_variavies[tabela_de_classificação[posicao+1][0]] == 'logico':
                    continue
                else:
                    return False, f"A variável {tabela_de_classificação[posicao-1][0]} é do tipo lógico e não pode receber {tabela_de_classificação[posicao+1][0]}."
            # Se o tipo da variável for numérico
            elif tipo == 'inteiro' or tipo == 'real':
                # Para o tipo numérico, é permitido atribuir outro numérico, um valor ou uma expressão
                # Se for um valor ou uma variável numérica, aceita
                if (tabela_de_classificação[posicao+1][1] == 'valor'
                    or (tabela_de_classificação[posicao+1][1] == 'var'
                        and (tabela_variavies[tabela_de_classificação[posicao+1][0]] == 'inteiro' or tabela_variavies[tabela_de_classificação[posicao+1][0]] == 'real'))):
                    continue
                # Se começar com um '(' é uma expressão, então testa se é válida
                elif tabela_de_classificação[posicao+1][1] == '(':
                    valores = []
                    pos_variaveis = posicao+2
                    while tabela_de_classificação[pos_variaveis][1] != ')':
                        if tabela_de_classificação[pos_variaveis][1] == 'var':
                            valores.append(tabela_variavies[tabela_de_classificação[pos_variaveis][0]])
                        elif tabela_de_classificação[pos_variaveis][1] == 'valor':
                            valores.append('valor')
                        pos_variaveis += 1
                    if any(x in valores for x in ['logico', 'caractere']):
                        return False, f"A variável {tabela_de_classificação[posicao-1][0]} é do tipo numérico e não pode receber uma expressão com variáveis lógicas ou de caractere."
                    # Se a expressão for válida, aceita
                    else:
                        continue
                else:
                    return False, f"A variável {tabela_de_classificação[posicao-1][0]} é do tipo numérico e só pode receber um valor, uma variável numérica ou uma expressão numérica."
            # Se o tipo da variável for mensagem
            elif tipo == 'caractere':
                # Para o tipo mensagem, é permitido atribuir outra mensagem ou uma variável de mensagem
                if (tabela_de_classificação[posicao+1][1] == 'msg'
                    or (tabela_de_classificação[posicao+1][1] == 'var'
                        and tabela_variavies[tabela_de_classificação[posicao+1][0]] == 'caractere')):
                    continue
                else:
                    return False, f"A variável {tabela_de_classificação[posicao-1][0]} é do tipo mensagem e só pode receber uma mensagem ou uma variável de caractere."
    
    # Se não houver erros, retorna True
    return True, "Análise semântica concluída com sucesso.", tabela_variavies