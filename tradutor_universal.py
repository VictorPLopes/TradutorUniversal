import csv  # Importa a biblioteca para trabalhar com arquivos CSV
import json  # Importa a biblioteca para trabalhar com arquivos JSON
import PySimpleGUI as sg  # Importa a biblioteca para trabalhar com a interface gráfica


VERSAO = "1.0.0"  # Versão do programa


# Variável global que controla o debug
debug = False


# Cria o dicionário de transição a partir de um arquivo CSV
# Função cria_transicao, com o parâmetro arquivo (nome do arquivo CSV)
def cria_transicao(nome_arquivo, debug=False):
    with open(nome_arquivo) as arquivo:  # Abre o arquivo CSV
        leitor = csv.reader(arquivo, delimiter=";")  # Lê o arquivo CSV

        # Cria uma lista de terminais a partir da primeira linha do arquivo CSV
        terminais = next(leitor)
        dicionario_transicao = {}  # Cria um dicionário vazio para armazenar as transições

        for linha in leitor:  # Para cada linha subsequente do arquivo CSV
            estado_atual = linha[0]  # O estado atual é o primeiro item da linha
            # Cria um dicionário vazio para a transição, com o estado atual como chave
            dicionario_transicao[estado_atual] = {}

            for i in range(1, len(linha)):  # Para cada novo estado (item) da linha
                if linha[i]:  # Se o item não for vazio
                    # Adiciona o novo estado no dicionário
                    dicionario_transicao[estado_atual][terminais[i]] = linha[i]

    if debug:  # Se o debug estiver ativado
        # Imprime o dicionário de transição
        print(f"DEBUG:\n    {dicionario_transicao}\n")

    return dicionario_transicao  # Retorna o dicionário de transição


# Definição do autômato
# Função automato, com os parâmetros: palavras, transicao (dicionário de transição), estado inicial padrão, estados finais e debug (para mostrar o estado atual e o próximo estado)
def automato_finito_deterministico(
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
def automato_pilha(
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

# Definição da analise semântica
def analise_semantica(resultado_sintatico):
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
        
        if declara: # se estiver declarando variável
            tabela_variavies[resultado_sintatico[posicao][0]] = resultado_sintatico[posicao+1][0] # adiciona a variável e seu tipo na tabela
            
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



# Definição da interface gráfica
# Definição da barra de menu
itens_menu = [["&Arquivo", ["&Novo", "---", "A&brir", "&Salvar", "---", "Sair"]], ["Analisadores", ["Simples", "Léxico", "Sintático"]]]

# Definição do layout
sg.theme("Topanga")  # Define o tema da interface gráfica
layout = [[sg.Menu(itens_menu)],
          [sg.Checkbox('Habilitar saída de debug', default=False, key="cb_debug")],
          [sg.Text("Entrada", size=(72, 1)), sg.Text("Saída")],
          [sg.Multiline("", key="entrada", size=(80, 40)), sg.Output(key="saida", size=(80, 40))],
          [sg.StatusBar(f"TradutorUniversal {VERSAO} - Reconhecedor de palavras, analisador e tradutor para C | Por Rodolfo H. R. Engelmann, Victor P. Lopes e Wilson B. R. Luo", relief=sg.RELIEF_SUNKEN, size=(80, 1))]]  # Define o layout da interface gráfica

# Cria a janela
janela = sg.Window(f"TradutorUniversal {VERSAO}", layout, finalize=True)

# Loop de eventos
while True:
    evento, valores = janela.read()  # type: ignore # Lê os eventos da janela
    
    # Controla o estado de debug
    if valores["cb_debug"]:
        debug = True
    else:
        debug = False

    match evento:  # Verifica o evento
        case sg.WIN_CLOSED:  # Se o evento for fechar a janela
            quit()  # Fecha o programa
        
        case "Sair":  # Se o evento for sair
            if sg.popup_yes_no("Deseja realmente sair?", title="Sair") == "YES":  # Pergunta se o usuário deseja sair
                quit()  # Fecha o programa
            
        case "Novo":  # Se o evento for novo
            janela["entrada"].update("")  # type: ignore # Limpa a entrada
            janela["saida"].update("")  # type: ignore # Limpa a saída

        case "Abrir":  # Se o evento for abrir
            caminho_arquivo = sg.popup_get_file("Selectione o arquivo de texto", title="Abrir",)  # Abre a janela para selecionar o arquivo
            if caminho_arquivo:  # Se o usuário selecionou um arquivo
                try:  # Tenta abrir o arquivo
                    with open(caminho_arquivo) as arquivo:  # Abre o arquivo
                        janela["entrada"].update(arquivo.read())  # type: ignore # Atualiza a entrada com o conteúdo do arquivo
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao abrir o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Salvar":  # Se o evento for salvar
            caminho_arquivo = sg.popup_get_file("Selectione o arquivo de texto", title="Salvar", save_as=True,)  # Abre a janela para selecionar o arquivo
            if caminho_arquivo:  # Se o usuário selecionou um arquivo
                try:  # Tenta abrir o arquivo
                    with open(caminho_arquivo, "w") as arquivo:  # Abre o arquivo
                        arquivo.writelines(valores["entrada"])  # Escreve o conteúdo da entrada no arquivo
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao salvar o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Simples":  # Se o evento for analisador simples
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    resultado = automato_finito_deterministico(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), debug=debug)  # Chama a função automato e armazena o resultado
                    print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao abrir o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Léxico":  # Se o evento for analisador léxico
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminho_pasta+"/tokens.json") as arquivo_tokens:  # Abre o arquivo
                        resultado = automato_finito_deterministico(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), json.load(arquivo_tokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                        
        case "Sintático":  # Se o evento for analisador sintático
            janela["saida"].update("")  # type: ignore # Limpa a saída
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminho_pasta+"/tokens.json") as arquivo_tokens:  # Abre o arquivo
                        resultado = automato_finito_deterministico(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), json.load(arquivo_tokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}\n\nCategorização:\n{resultado[2]}")  # Atualiza a saída com o resultado
                    if not len(resultado[0]):
                        try:  # Tenta abrir o arquivo
                            with open(caminho_pasta+"/pilha.json") as arquivo_transicao_pilha: # Abre o arquivo
                                print() # Pula uma linha
                                if automato_pilha(resultado[1], json.load(arquivo_transicao_pilha), debug=debug): # Chama a função e exibe o resultado
                                    print("\nAceito (Léxico e Sintático)")
                                else:
                                    print("Rejeitado (Sintático)")
                        except Exception as e:  # Se ocorrer uma exceção
                            sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    else:
                        print("Rejeitado (Léxico)")
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro