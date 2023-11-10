VERSAO = "1.0.0"  # Versão do programa

import csv  # Importa a biblioteca para trabalhar com arquivos CSV
import json  # Importa a biblioteca para trabalhar com arquivos JSON
import PySimpleGUI as sg  # Importa a biblioteca para trabalhar com a interface gráfica


# Variável global que controla o debug
debug = False


# Cria o dicionário de transição a partir de um arquivo CSV
# Função criaTransicao, com o parâmetro arquivo (nome do arquivo CSV)
def criaTransicao(nomeArquivo, debug=False):
    with open(nomeArquivo) as arquivo:  # Abre o arquivo CSV
        leitor = csv.reader(arquivo, delimiter=";")  # Lê o arquivo CSV

        # Cria uma lista de terminais a partir da primeira linha do arquivo CSV
        terminais = next(leitor)
        dicionarioTransicao = {}  # Cria um dicionário vazio para armazenar as transições

        for linha in leitor:  # Para cada linha subsequente do arquivo CSV
            estadoAtual = linha[0]  # O estado atual é o primeiro item da linha
            # Cria um dicionário vazio para a transição, com o estado atual como chave
            dicionarioTransicao[estadoAtual] = {}

            for i in range(1, len(linha)):  # Para cada novo estado (item) da linha
                if linha[i]:  # Se o item não for vazio
                    # Adiciona o novo estado no dicionário
                    dicionarioTransicao[estadoAtual][terminais[i]] = linha[i]

    if debug:  # Se o debug estiver ativado
        # Imprime o dicionário de transição
        print(f"DEBUG:\n    {dicionarioTransicao}\n")

    return dicionarioTransicao  # Retorna o dicionário de transição


# Definição do autômato
# Função autômato, com os parâmetros: palavras, transicao (dicionário de transição), estado inicial padrão, estados finais e debug (para mostrar o estado atual e o próximo estado)
def automatoFinitoDeterministico(
    palavras,
    transicao,
    tokens=None,
    estadoInicial="q0",
    estadosFinais="qf",
    palavrasReservadas="qf1",
    debug=False,
):
    palavrasAceitas = []  # Lista de palavras aceitas, inicialmente vazia
    palavrasRejeitadas = []  # Lista de palavras rejeitadas, inicialmente vazia
    categorizacao = [] # Categorização das palavras aceitas
    
    for palavra in palavras:  # Para cada palavra na lista de palavras
        estadoAtual = estadoInicial  # Volta para o estado inicial

        try:  # Pode ocorrer uma exceção (erro) para palavras que não são reconhecidas
            for letra in palavra:  # Para cada letra da palavra
                if debug:  # Se o debug estiver ativado
                    # Estado atual e a letra lida
                    print(f'DEBUG:\n    Estado atual: "{estadoAtual}" | letra: {letra} | palavra: {palavra}')

                # Novo estado, partindo do estado atual e da letra lida
                estadoAtual = transicao[estadoAtual][letra]

                if debug:
                    # Próximo estado
                    print(f"    Proximo estado: {estadoAtual}")
            # Sai do for ao ler toda a palavra

            # Se não alcançar o estado final - rejeita a palavra
            if not estadoAtual.startswith(estadosFinais):
                palavrasRejeitadas.append([palavra, "Não alcançou um estado final"])  # Adiciona a palavra à lista de palavras rejeitadas
                continue  # Vai para a próxima palavra

            # Se alcançar o estado final mas não foi solicitada a análise léxica
            if not tokens:  # Caso não seja feita a análise léxica
                palavrasAceitas.append(palavra)  # Adiciona a palavra à lista de palavras aceitas
                continue  # Vai para a próxima palavra

            # Se alcançar o estado final e foi solicitada a análise léxica
            if estadoAtual != palavrasReservadas:  # Se não for o estado final das palavras reservadas
                palavrasAceitas.append([palavra, tokens[estadoAtual]])  # Adiciona a palavra e o token à tabela de símbolos
                categorizacao.append(tokens[estadoAtual]) # Adiciona a categoria da palavra à lista de categorização
                continue  # Vai para a próxima palavra
            if palavra in tokens[palavrasReservadas]:  # Se a palavra estiver na lista de palavras reservadas
                palavrasAceitas.append([palavra, palavra])  # Adiciona a palavra e o token à tabela de símbolos
                categorizacao.append(palavra) # Adiciona a categoria da palavra à lista de categorização
            else:  # Se a palavra não estiver na lista de palavras reservadas, é um nome de variável
                palavrasAceitas.append([palavra, "var"])  # Adiciona a palavra e o token à tabela de símbolos
                categorizacao.append([palavra, "var"])  # Adiciona a palavra à lista de categorização

        except:  # Se ocorrer uma exceção
            # Rejeita a palavra
            palavrasRejeitadas.append([palavra, "Transição de estados inválida presente"])  # Adiciona a palavra à lista de palavras rejeitadas
            continue  # Vai para a próxima palavra

    # Retorna a lista de palavras reconhecidas
    return palavrasRejeitadas, palavrasAceitas, categorizacao

# Definição do autômato com pilha
def automatoPilha(
    cadeia,
    transicaoPilha,
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
            pilha.extend(reversed(transicaoPilha[terminal[1]][topo]))
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
def analiseSemantica(resultadoSintatico):
    tabelaVariavies = {}  # dicionário vazio

    declara = False # controla a declaração de variáveis

    # vamos percorrer o resultado_sintatico
    # em busca de ['var','var'] que indica
    # a sessão de declaração de variáveis
    # que termina com ['inicio','inicio']
    # temos que buscar pelo terminal[0] = 'var'
    # e finalizar a busca com o terminal[0] = 'inicio'

    for posicao in range(len(resultadoSintatico)):

        if resultadoSintatico[posicao][0] == 'var': # declarações da variáveis
            declara = True # inicia a etapa de declaração de variáveis
            continue # passa para a próxima posição

        if resultadoSintatico[posicao][0] == 'inicio':
            declara = False  # finaliza a busca
        
        if declara: # se estiver declarando variável
            tabelaVariavies[resultadoSintatico[posicao][0]] = resultadoSintatico[posicao+1][0] # adiciona a variável e seu tipo na tabela
            
        elif resultadoSintatico[posicao][1] == 'var':
            var = resultadoSintatico[posicao][0]
            if var in tabelaVariavies:
                if tabelaVariavies[var] is 'logico':
                    if resultadoSintatico[posicao-2][1] == 'leia':
                        return False, f"Variável {var} não é um tipo válido para leitura."
                    else:
                        continue
            else:
                return False, f"Variável {var} não declarada."
            
        elif resultadoSintatico[posicao][1] == 'op_atrib':
            tipo = tabelaVariavies[resultadoSintatico[posicao-1][0]]
            if tipo == 'logico':
                if resultadoSintatico[posicao+1][1] == 'verdadeiro' or resultadoSintatico[posicao+1][1] == 'falso' or tabelaVariavies[resultadoSintatico[posicao+1][0]] == 'logico':
                    continue
                else:
                    return False, "Atribuição inválida para variável lógica."
            elif tipo == 'inteiro' or tipo == 'real':
                if (resultadoSintatico[posicao+1][1] == 'valor'
                    or (resultadoSintatico[posicao+1][1] == 'var'
                        and (tabelaVariavies[resultadoSintatico[posicao+1][0]] == 'inteiro' or tabelaVariavies[resultadoSintatico[posicao+1][0]] == 'real'))):
                    continue
                elif resultadoSintatico[posicao+1][1] == '(':
                    valores = []
                    posVariaveis = posicao+2
                    while resultadoSintatico[posVariaveis][1] != ')':
                        if resultadoSintatico[posVariaveis][1] == 'var':
                            valores.append(tabelaVariavies[resultadoSintatico[posVariaveis][0]])
                        elif resultadoSintatico[posVariaveis][1] == 'valor':
                            valores.append('valor')
                    if all(x in valores for x in ['logico', 'msg']):
                        return False, "Valores inválidos na expressão de atribuição."
                    else:
                        continue
                else:
                    return False, "Atribuição inválida para variável numérica."
            elif tipo == 'msg':
                if (resultadoSintatico[posicao+1][1] == 'msg'
                    or (resultadoSintatico[posicao+1][1] == 'var'
                        and tabelaVariavies[resultadoSintatico[posicao+1][0]] == 'msg')):
                    continue
                else:
                    return False, "Atribuição inválida para variável de mensagem."
            


# Definição da interface gráfica
# Definição da barra de menu
itensMenu = [["&Arquivo", ["&Novo", "---", "A&brir", "&Salvar", "---", "Sair"]], ["Analisadores", ["Simples", "Léxico", "Sintático"]]]

# Definição do layout
sg.theme("Topanga")  # Define o tema da interface gráfica
layout = [[sg.Menu(itensMenu)],
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
            caminhoArquivo = sg.popup_get_file("Selectione o arquivo de texto", title="Abrir",)  # Abre a janela para selecionar o arquivo
            if caminhoArquivo:  # Se o usuário selecionou um arquivo
                try:  # Tenta abrir o arquivo
                    with open(caminhoArquivo) as arquivo:  # Abre o arquivo
                        janela["entrada"].update(arquivo.read())  # type: ignore # Atualiza a entrada com o conteúdo do arquivo
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao abrir o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Salvar":  # Se o evento for salvar
            caminhoArquivo = sg.popup_get_file("Selectione o arquivo de texto", title="Salvar", save_as=True,)  # Abre a janela para selecionar o arquivo
            if caminhoArquivo:  # Se o usuário selecionou um arquivo
                try:  # Tenta abrir o arquivo
                    with open(caminhoArquivo, "w") as arquivo:  # Abre o arquivo
                        arquivo.writelines(valores["entrada"])  # Escreve o conteúdo da entrada no arquivo
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao salvar o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Simples":  # Se o evento for analisador simples
            caminhoPasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminhoPasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    resultado = automatoFinitoDeterministico(valores["entrada"].split(), criaTransicao(caminhoPasta+"/transicao.csv"), debug=debug)  # Chama a função automato e armazena o resultado
                    print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao abrir o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Léxico":  # Se o evento for analisador léxico
            caminhoPasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminhoPasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminhoPasta+"/tokens.json") as arquivoTokens:  # Abre o arquivo
                        resultado = automatoFinitoDeterministico(valores["entrada"].split(), criaTransicao(caminhoPasta+"/transicao.csv"), json.load(arquivoTokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                        
        case "Sintático":  # Se o evento for analisador sintático
            janela["saida"].update("")  # type: ignore # Limpa a saída
            caminhoPasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminhoPasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminhoPasta+"/tokens.json") as arquivoTokens:  # Abre o arquivo
                        resultado = automatoFinitoDeterministico(valores["entrada"].split(), criaTransicao(caminhoPasta+"/transicao.csv"), json.load(arquivoTokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}\n\nCategorização:\n{resultado[2]}")  # Atualiza a saída com o resultado
                    if not len(resultado[0]):
                        try:  # Tenta abrir o arquivo
                            with open(caminhoPasta+"/pilha.json") as arquivoTransicaoPilha: # Abre o arquivo
                                print() # Pula uma linha
                                if automatoPilha(resultado[1], json.load(arquivoTransicaoPilha), debug=debug): # Chama a função e exibe o resultado
                                    print("\nAceito (Léxico e Sintático)")
                                else:
                                    print("Rejeitado (Sintático)")
                        except Exception as e:  # Se ocorrer uma exceção
                            sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    else:
                        print("Rejeitado (Léxico)")
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro