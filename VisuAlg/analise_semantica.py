# Definição da analise semântica
def analise_semantica(resultado_sintatico, debug = False):
    tabela_variavies = {}  # dicionário vazio

    declara = False # controla a declaração de variáveis

    # vamos percorrer o resultado_sintatico
    # em busca de ['var','var'] que indica
    # a sessão de declaração de variáveis
    # que termina com ['inicio','inicio']
    # temos que buscar pelo terminal[0] = 'var'
    # e finalizar a busca com o terminal[0] = 'inicio'

    for posicao in range(len(resultado_sintatico)):

        if resultado_sintatico[posicao][0] == 'var': # declarações da variáveis
            declara = True # inicia a etapa de declaração de variáveis
            continue # passa para a próxima posição

        if resultado_sintatico[posicao][0] == 'inicio':
            declara = False  # finaliza a busca
            if debug:
                print("Tabela de variáveis:\n", tabela_variavies)
        
        if declara: # se estiver declarando variável
            tabela_variavies[resultado_sintatico[posicao][0]] = resultado_sintatico[posicao+1][0] # adiciona a variável e seu tipo na tabela
            
        # Se o debug estiver ativado, imprime o lexema e o token da posição atual
        if debug:
            print(resultado_sintatico[posicao])
            
        # Quando lê uma variável
        elif resultado_sintatico[posicao][1] == 'var':
            # Salva o nome da variável e checa se está na tabela de variáveis
            var = resultado_sintatico[posicao][0]
            if var in tabela_variavies:
                # Se o tipo da variável for lógico
                if tabela_variavies[var] is 'logico':
                    # Se houver um leia antes, rejeita
                    if resultado_sintatico[posicao-2][1] == 'leia':
                        return False, f"Variável {var} não é um tipo válido para leitura."
                    # Se houver um compara antes, testa se está comparando corretamente
                    elif resultado_sintatico[posicao-1][1] == 'compara':
                        # Para o tipo lógico, só é permitido comparar igualdade ou diferença com outro lógico ou com verdadeiro ou falso
                        if resultado_sintatico[posicao-1][0] == '==' or resultado_sintatico[posicao-1][0] == '<>':
                            if (resultado_sintatico[posicao-2][1] == 'verdadeiro' or resultado_sintatico[posicao-2][1] == 'falso') or tabela_variavies[resultado_sintatico[posicao-2][0]] == 'logico':
                                continue
                            else:
                                return False, "Comparação inválida para variável lógica."
                # Se o tipo da variável for numérico
                elif tabela_variavies[var] is 'inteiro' or tabela_variavies[var] is 'real':
                    # Caso especial para o tipo inteiro no comando para
                    if resultado_sintatico[posicao-1][1] == 'para':
                        if tabela_variavies[var] is 'inteiro':
                            # Testa se o intervalo é válido
                            if resultado_sintatico[posicao+2][0] < resultado_sintatico[posicao+4][0]:
                                continue
                            else:
                                return False, "Intervalo inválido no comando para."
                        else:
                            return False, "Variável de iteração deve ser do tipo inteiro."
                    # Se houver um leia antes, aceita
                    if resultado_sintatico[posicao-1][1] == 'leia':
                        continue
                    # Se houver um compara antes, testa se está comparando corretamente
                    elif resultado_sintatico[posicao-1][1] == 'compara':
                        # Para o tipo numérico, é permitido comparar igualdade, diferença, maior, menor, maior ou igual e menor ou igual com outro numérico
                        if resultado_sintatico[posicao-2][1] == 'valor' or (tabela_variavies[resultado_sintatico[posicao-2][0]] == 'inteiro' or tabela_variavies[resultado_sintatico[posicao-2][0]] == 'real'):
                            continue
                        else:
                            return False, "Comparação inválida para variável numérica."
                # Se o tipo da variável for mensagem
                elif tabela_variavies[var] is 'msg':
                    # Se houver um leia antes, aceita
                    if resultado_sintatico[posicao-1][1] == 'leia':
                        continue
                    # Se houver um compara antes, rejeita
                    elif resultado_sintatico[posicao-1][1] == 'compara':
                        return False, "Comparação inválida para variável de mensagem."
                    
            else:
                return False, f"Variável {var} não declarada."
            
        # Quando lê um operador de atribuição
        elif resultado_sintatico[posicao][1] == 'atrib':
            # Salva o tipo da variável
            tipo = tabela_variavies[resultado_sintatico[posicao-1][0]]
            # Se o tipo da variável for lógica
            if tipo == 'logico':
                # Para o tipo lógico, só é permitido atribuir verdadeiro, falso ou outro lógico
                if resultado_sintatico[posicao+1][1] == 'verdadeiro' or resultado_sintatico[posicao+1][1] == 'falso' or tabela_variavies[resultado_sintatico[posicao+1][0]] == 'logico':
                    continue
                else:
                    return False, "Atribuição inválida para variável lógica."
            # Se o tipo da variável for numérico
            elif tipo == 'inteiro' or tipo == 'real':
                # Para o tipo numérico, é permitido atribuir outro numérico, um valor ou uma expressão
                # Se for um valor ou uma variável numérica, aceita
                if (resultado_sintatico[posicao+1][1] == 'valor'
                    or (resultado_sintatico[posicao+1][1] == 'var'
                        and (tabela_variavies[resultado_sintatico[posicao+1][0]] == 'inteiro' or tabela_variavies[resultado_sintatico[posicao+1][0]] == 'real'))):
                    continue
                # Se começar com um '(' é uma expressão, então testa se é válida
                elif resultado_sintatico[posicao+1][1] == '(':
                    valores = []
                    pos_variaveis = posicao+2
                    while resultado_sintatico[pos_variaveis][1] != ')':
                        if resultado_sintatico[pos_variaveis][1] == 'var':
                            valores.append(tabela_variavies[resultado_sintatico[pos_variaveis][0]])
                        elif resultado_sintatico[pos_variaveis][1] == 'valor':
                            valores.append('valor')
                    if all(x in valores for x in ['logico', 'msg']):
                        return False, "Valores inválidos na expressão de atribuição."
                    # Se a expressão for válida, aceita
                    else:
                        continue
                else:
                    return False, "Atribuição inválida para variável numérica."
            # Se o tipo da variável for mensagem
            elif tipo == 'msg':
                # Para o tipo mensagem, é permitido atribuir outra mensagem ou uma variável de mensagem
                if (resultado_sintatico[posicao+1][1] == 'msg'
                    or (resultado_sintatico[posicao+1][1] == 'var'
                        and tabela_variavies[resultado_sintatico[posicao+1][0]] == 'msg')):
                    continue
                else:
                    return False, "Atribuição inválida para variável de mensagem."
    
    # Se não houver erros, retorna True
    return True, "Análise semântica concluída com sucesso."