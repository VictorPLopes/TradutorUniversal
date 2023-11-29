# Definição do autômato
# Função automato, com os parâmetros: palavras, transicao (dicionário de transição), estado inicial padrão, estados finais e debug (para mostrar o estado atual e o próximo estado)
def analise_lexica(
    palavras,
    transicao,
    tokens=None,
    estado_inicial="q0",
    estados_finais="qf",
    palavras_reservadas="qf1",
    debug=False,
):
    palavras_aceitas = []  # Lista de palavras aceitas, inicialmente vazia
    palavras_rejeitadas = []  # Lista de palavras rejeitadas, inicialmente vazia
    categorizacao = [] # Categorização das palavras aceitas
    
    for palavra in palavras:  # Para cada palavra na lista de palavras
        estado_atual = estado_inicial  # Volta para o estado inicial

        try:  # Pode ocorrer uma exceção (erro) para palavras que não são reconhecidas
            for letra in palavra:  # Para cada letra da palavra
                if debug:  # Se o debug estiver ativado
                    # Estado atual e a letra lida
                    print(f'DEBUG:\n    Estado atual: "{estado_atual}" | letra: {letra} | palavra: {palavra}')

                # Novo estado, partindo do estado atual e da letra lida
                estado_atual = transicao[estado_atual][letra]

                if debug:
                    # Próximo estado
                    print(f"    Proximo estado: {estado_atual}")
            # Sai do for ao ler toda a palavra

            # Se não alcançar o estado final - rejeita a palavra
            if not estado_atual.startswith(estados_finais):
                palavras_rejeitadas.append([palavra, "Não alcançou um estado final"])  # Adiciona a palavra à lista de palavras rejeitadas
                continue  # Vai para a próxima palavra

            # Se alcançar o estado final mas não foi solicitada a análise léxica
            if not tokens:  # Caso não seja feita a análise léxica
                palavras_aceitas.append(palavra)  # Adiciona a palavra à lista de palavras aceitas
                continue  # Vai para a próxima palavra

            # Se alcançar o estado final e foi solicitada a análise léxica
            if estado_atual != palavras_reservadas:  # Se não for o estado final das palavras reservadas
                palavras_aceitas.append([palavra, tokens[estado_atual]])  # Adiciona a palavra e o token à tabela de símbolos
                categorizacao.append(tokens[estado_atual]) # Adiciona a categoria da palavra à lista de categorização
                continue  # Vai para a próxima palavra
            if palavra in tokens[palavras_reservadas]:  # Se a palavra estiver na lista de palavras reservadas
                palavras_aceitas.append([palavra, palavra])  # Adiciona a palavra e o token à tabela de símbolos
                categorizacao.append(palavra) # Adiciona a categoria da palavra à lista de categorização
            else:  # Se a palavra não estiver na lista de palavras reservadas, é um nome de variável
                palavras_aceitas.append([palavra, "var"])  # Adiciona a palavra e o token à tabela de símbolos
                categorizacao.append([palavra, "var"])  # Adiciona a palavra à lista de categorização

        except:  # Se ocorrer uma exceção
            # Rejeita a palavra
            palavras_rejeitadas.append([palavra, "Transição de estados inválida presente"])  # Adiciona a palavra à lista de palavras rejeitadas
            continue  # Vai para a próxima palavra

    # Retorna a lista de palavras reconhecidas
    return palavras_rejeitadas, palavras_aceitas, categorizacao

# Definição do autômato com pilha
def analise_sintatica(
    cadeia,
    transicao_pilha,
    estado="q1", # as trnsição do autômato com pilha ocorrem no estado q1
    debug=False
):
    # a transição de q0 para q1 acrescenta a variável S no topo pilha
    pilha = ['S']

    try:
        # vai percorrer os terminais da cadeia de entrada sempre buscando uma transição para o terminal
        for terminal in cadeia:
            topo = pilha.pop()   # remove o elemento do topo da pilha
            if debug:
                print(' terminal: ', terminal[1], ' topo da pilha: ', topo)
            pilha.extend(reversed(transicao_pilha[terminal[1]][topo]))
            if debug:
                print('Pilha: ', pilha)

        # percorri todos os terminais da cadeia - significa
        # que a cadeia está vazia
        if not len(pilha):   # a pilha está vazia
            estado = 'qf'
        # se eu li a cadeia pórem a pilha não estiver vazia não vou para qf e a cadeia rejeita
        if estado != 'qf':
            return False

    # caso leia uma terminal na cadeia não existe nenhuma transição definida para esse terminal
    # a leitura de terminais da cadeia pára
    except:
        return False
    return True