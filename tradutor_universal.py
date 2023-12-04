import csv  # Importa a biblioteca para trabalhar com arquivos CSV
import json  # Importa a biblioteca para trabalhar com arquivos JSON
import PySimpleGUI as sg  # Importa a biblioteca para trabalhar com a interface gráfica
import importlib # Importa a biblioteca para trabalhar com a importação de módulos
import importlib.util # Importa a biblioteca para trabalhar com a importação de módulos
import sys  # Importa a biblioteca para trabalhar com o sistema

import analisadores  # Importa o módulo analisadores


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


# Definição da interface gráfica
# Definição da barra de menu
itens_menu = [["&Arquivo", ["&Novo", "---", "A&brir", "&Salvar", "---", "Sair"]], ["Analisadores", ["Simples", "Léxico", "Sintático", "Semântico"]], ["Traduzir", ["Executar"]]]

# Definição do layout
sg.theme("Topanga")  # Define o tema da interface gráfica
layout = [[sg.Menu(itens_menu)],
          [sg.Checkbox('Habilitar saída de debug', default=False, key="cb_debug"), sg.Button("Salvar Saída", size=(10, 1), key="bt_salvar")],
          [sg.Text("Entrada", size=(72, 1)), sg.Text("Saída")],
          [sg.Multiline("", key="entrada", size=(80, 40)), sg.Output(key="saida", size=(80, 40), )],
          [sg.StatusBar(f"TradutorUniversal {VERSAO} - Reconhecedor de palavras, analisador e tradutor modular | Por Rodolfo H. R. Engelmann, Victor P. Lopes e Wilson B. R. Luo", relief=sg.RELIEF_SUNKEN, size=(80, 1))]]  # Define o layout da interface gráfica

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
            caminho_arquivo = sg.popup_get_file("Selecione o local para salvar o texto", title="Salvar", save_as=True,)  # Abre a janela para selecionar o arquivo
            if caminho_arquivo:  # Se o usuário selecionou um arquivo
                try:  # Tenta abrir o arquivo
                    with open(caminho_arquivo, "w") as arquivo:  # Abre o arquivo
                        arquivo.writelines(valores["entrada"])  # Escreve o conteúdo da entrada no arquivo
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao salvar o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
        
        case "bt_salvar":  # Se o evento for salvar saída
            caminho_arquivo = sg.popup_get_file("Selecione o local para salvar o texto", title="Salvar", save_as=True,)  # Abre a janela para selecionar o arquivo
            if caminho_arquivo:  # Se o usuário selecionou um arquivo
                try:  # Tenta abrir o arquivo
                    with open(caminho_arquivo, "w") as arquivo:  # Abre o arquivo
                        texto_saida = janela["saida"].get()  # type: ignore # Armazena o conteúdo da saída
                        arquivo.writelines(texto_saida)  # Escreve o conteúdo da saída no arquivo
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao salvar o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Simples":  # Se o evento for analisador simples
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    resultado = analisadores.analise_lexica(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), debug=debug)  # Chama a função automato e armazena o resultado
                    print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro ao abrir o arquivo:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Léxico":  # Se o evento for analisador léxico
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminho_pasta+"/tokens.json") as arquivo_tokens:  # Abre o arquivo
                        resultado = analisadores.analise_lexica(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), json.load(arquivo_tokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                        
        case "Sintático":  # Se o evento for analisador sintático
            janela["saida"].update("")  # type: ignore # Limpa a saída
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminho_pasta+"/tokens.json") as arquivo_tokens:  # Abre o arquivo
                        resultado = analisadores.analise_lexica(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), json.load(arquivo_tokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                    if not len(resultado[0]):
                        try:  # Tenta abrir o arquivo
                            with open(caminho_pasta+"/pilha.json") as arquivo_transicao_pilha: # Abre o arquivo
                                print() # Pula uma linha
                                if analisadores.analise_sintatica(resultado[1], json.load(arquivo_transicao_pilha), debug=debug): # Chama a função e exibe o resultado
                                    print("\nAceito (Léxico e Sintático)")
                                else:
                                    print("Rejeitado (Sintático)")
                        except Exception as e:  # Se ocorrer uma exceção
                            sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    else:
                        print("Rejeitado (Léxico)")
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    
        case "Semântico":  # Se o evento for analisador semântico
            janela["saida"].update("")  # type: ignore # Limpa a saída
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminho_pasta+"/tokens.json") as arquivo_tokens:  # Abre o arquivo
                        resultado = analisadores.analise_lexica(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), json.load(arquivo_tokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                    if not len(resultado[0]):
                        try:  # Tenta abrir o arquivo
                            with open(caminho_pasta+"/pilha.json") as arquivo_transicao_pilha: # Abre o arquivo
                                print() # Pula uma linha
                                if analisadores.analise_sintatica(resultado[1], json.load(arquivo_transicao_pilha), debug=debug): # Chama a função e exibe o resultado
                                    print("\nAceito (Léxico e Sintático)")
                                    # Se o programa for aceito, chama a função para análise semântica
                                    
                                    # Cria um módulo
                                    spec = importlib.util.spec_from_file_location("analise_semantica", caminho_pasta+"/analise_semantica.py")
                                    module = importlib.util.module_from_spec(spec)  # type: ignore # Add type hint to spec parameter
                                    sys.modules["analise_semantica"] = module
                                    spec.loader.exec_module(module)  # type: ignore # Add type hint to spec parameter
                                
                                    resultado_semantico = module.analise_semantica(resultado[1], debug=debug) # Chama a função de análise semântica
                                    print(f"\n{resultado_semantico[1]}")
                                    # Se houver erros na análise semântica
                                    if not resultado_semantico[0]:
                                        print("\nRejeitado (Semântico)")
                                    else:
                                        print("\nAceito (Semântico, Léxico e Sintático)")
                                else:
                                    print("Rejeitado (Sintático)")
                        except Exception as e:  # Se ocorrer uma exceção
                            sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    else:
                        print("Rejeitado (Léxico)")
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
        
        case "Executar":  # Se o evento for analisador semântico
            janela["saida"].update("")  # type: ignore # Limpa a saída
            caminho_pasta = sg.popup_get_folder("Selectione a pasta da linguagem", title="Abrir")  # Abre a janela para selecionar a pasta
            if caminho_pasta:  # Se o usuário selecionou uma pasta
                try:  # Tenta abrir o arquivo
                    with open(caminho_pasta+"/tokens.json") as arquivo_tokens:  # Abre o arquivo
                        resultado = analisadores.analise_lexica(valores["entrada"].split(), cria_transicao(caminho_pasta+"/transicao.csv"), json.load(arquivo_tokens), debug=debug)  # Chama a função automato e armazena o resultado
                        print(f"Palavras rejeitadas:\n{resultado[0]}\n\nPalavras aceitas:\n{resultado[1]}")  # Atualiza a saída com o resultado
                    if not len(resultado[0]):
                        try:  # Tenta abrir o arquivo
                            with open(caminho_pasta+"/pilha.json") as arquivo_transicao_pilha: # Abre o arquivo
                                print() # Pula uma linha
                                if analisadores.analise_sintatica(resultado[1], json.load(arquivo_transicao_pilha), debug=debug): # Chama a função e exibe o resultado
                                    print("\nAceito (Léxico e Sintático)")
                                    # Se o programa for aceito, chama a função para análise semântica
                                    
                                    # Cria um módulo
                                    spec = importlib.util.spec_from_file_location("analise_semantica", caminho_pasta+"/analise_semantica.py")
                                    module = importlib.util.module_from_spec(spec)  # type: ignore # Add type hint to spec parameter
                                    sys.modules["analise_semantica"] = module
                                    spec.loader.exec_module(module)  # type: ignore # Add type hint to spec parameter
                                
                                    resultado_semantico = module.analise_semantica(resultado[1], debug=debug) # Chama a função de análise semântica
                                    print(f"\n{resultado_semantico[1]}")
                                    # Se houver erros na análise semântica
                                    if not resultado_semantico[0]:
                                        print("\nRejeitado (Semântico)")
                                    else:
                                        print("\nAceito (Semântico, Léxico e Sintático)")
                                        # Chama o tradutor
                                        janela["saida"].update("") # type: ignore # Limpa a saída
                                        
                                        # Cria um módulo
                                        spec = importlib.util.spec_from_file_location("tradutor", caminho_pasta+"/tradutor.py")
                                        module = importlib.util.module_from_spec(spec)  # type: ignore # Add type hint to spec parameter
                                        sys.modules["tradutor"] = module
                                        spec.loader.exec_module(module) # type: ignore # Add type hint to spec parameter
                                        
                                        # Mostra o código traduzido
                                        print(module.tradutor(resultado[1], resultado_semantico[2]))
                                else:
                                    print("Rejeitado (Sintático)")
                        except Exception as e:  # Se ocorrer uma exceção
                            sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro
                    else:
                        print("Rejeitado (Léxico)")
                except Exception as e:  # Se ocorrer uma exceção
                    sg.popup_error(f"Erro:\n{e}", title="Erro")  # Exibe uma mensagem de erro