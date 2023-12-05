# TradutorUniversal

Ferramenta que possibilita, de forma mais fácil, a criação e execução de analisadores (léxicos, sintáticos e semânticos) para qualquer linguagem de programação e a tradução de seu código para qualquer outra linguagem. A ferramenta inclui um módulo de exemplo já pronto que analisa e traduz código de uma versão simplificada da liguagem VisuAlg (modificada pelo Prof. Dr. Osvaldo Severino Junior para fins didáticos) para a linguagem C.
</br>
O projeto foi criado por Rodolfo Henrique Raymundo Engelmann, Victor Probio Lopes e Wilson Bin Rong Luo para uso na disciplina de Compiladores, do 5º semestre do curso de Engenharia de Computação do Instituto Federal de Educação, Ciência e Tecnologia de São Paulo, Campus Piracicaba. Partes do código foram baseadas nos algoritmos originais do Prof. ministrante da disciplina, Dr. Osvaldo Severino Junior.

## Uso

Antes de tudo, é necessário ter instalado uma versão recente (3.10 ou superior) do Python instalada, além das bibliotecas `csv`, `json`, `PySimpleGUI`, `importlib`e `sys`. Para obter o programa basta clonar o repositório ou baixar a _release_ mais nova do _software_. A aplicaçõ deve ser executada através do arquivo `tradutor_universal.py`.
</br>
A interface visual é simples de usar. A tela é dividida ao meio, com duas caixas de texto: uma, à esquerda, para entrada e outra, à direita, para saída. O código para análise deve ser inserido na caixa da esquerda. Na parte superior da janela há um menu, com as categorias de `Arquivo`, `Analisadores` e `Traduzir`. É possível carregar um arquivo de texto já existente para análise, bastando navegar até `Arquivo` > `Abrir`, e usar a opção `Browse` na nova janela de _pop-up_ para escolher o arquivo a ser carregado. Na mesma categoria, é possível limpar a entrada com o botão `Novo`, `Salvar` a entrada para um arquivo ou `Sair` do programa. As análises de código são feitas através da categoria `Analisadores` e a tradução é feita em `Traduzir` > `Executar`. Por fim, a opção `Habilitar saída de debug` habilita uma saída mais detalhada, enquanto o botão `Salvar Saída` permite salvar os dados da caixa de texto direita (como código traduzido) para um arquivo externo.

![image](https://github.com/VictorPLopes/TradutorUniversal/assets/77900343/5c94ed28-c241-42ea-9be3-930709a3ea7b)

### Analisando e traduzindo uma linguagem já definida (exemplo com VisuAlg)

A pasta `\EXEMPLOS\VisuAlg_para_C` contém as definições da linguagem VisuAlg, com várias modificações e simplificações para tornar suas definições mais simples para fins didáticos, além da implementação de um tradutor para a linguagem de programação C. No momento, essa versão só suporta os seguintes comandos:

- Definição de variáveis
- Atribuição de variáveis
- Leitura de entrada do teclado
- Escrita de caracteres no teminal
- Se e senão
- Comando de repetição `para`
- Comando de repetição `enquanto`

Antes de executar uma análise ou tradução, é necessário digitar ou carregar um código no campo de entrada. O arquivo `\EXEMPLOS\VisuAlg_para_C\teste.txt` pode ser usado para testar a linguagem VisuAlg.

![image](https://github.com/VictorPLopes/TradutorUniversal/assets/77900343/fd09daf7-81bc-4429-9a87-c9c2eb3ecfdb)

Com o código carregado é possível executar uma das seguintes análises (pelo menu `Analisadores`)

1. Análise Simples
   - Análisa se as cadeias (palavras) da entrada são todas válidas na linguagem definida
2. Análise Léxica
   - Análise Simples + categorização dos lexemas (palavras) em tokens (categorias) da linguagem definida
3. Análise Sintática
   - Análise Léxica + verificação da sintaxe (estrutura) do código
4. Análise Semântica
   - Análise Sintática + verificação da semântica (lógica) do cógigo. Exemplos: verificação de atribuição, escrita e leitura com base no tipo da variável, validação de intervalos etc.

Para qualquer um dos analisadores selecionados, é necessário escolher, no pop-up, a pasta onde estão os arquivos de definição da linguagem. Para o exemplo do VisuAlg, essa pasta é `\EXEMPLOS\VisuAlg_para_C`. Ao executar um dos analisadores, o resultado da análise é exibido na caixa de texto da direita.

![image](https://github.com/VictorPLopes/TradutorUniversal/assets/77900343/25c114f9-1d67-469f-8f53-075afc6722c5)

A tradução segue a mesma lógica. Ao clicar em `Traduzir` > `Executar` o programa realiza uma Análise Semântica, e se essa for bem sucedida traduz o código para outra linguagem definida. Para o exemplo, a tradução é feita entre VisuAlg e C.

![image](https://github.com/VictorPLopes/TradutorUniversal/assets/77900343/d0c6f3a5-89a6-4f6e-84b0-13f55cb9dae3)

Essa saída pode ser salva com o botão `Salvar Saída`.

### Definindo uma nova linguagem

Para criar um novo módulo, ou seja, a definição de uma nova linguagem, é necessário antes de tudo, criar uma nova pasta onde os arquivos da linguagem serão salvos. Nessa pasta, devem estar alguns arquivos para garantir o funcionamento de cada funcionalidade do programa:

1. Para a Análise Simples
   - Arquivo `transicao.csv`
2. Para a Análise Léxica
   - Arquivos da Análise Simples
   - Arquivo `tokens.json`
3. Para a Análise Sintática
   - Arquivos da Análise Léxica
   - Arquivo `pilha.json`
4. Para a Análise Semântica
   - Arquivos da Análise Sintática
   - Arquivo `analise_semantica.py` e arquivo vazio de nome `__init__.py`
5. Para a Tradução
   - Arquivos da Análise Semântica
   - Arquivo `tradutor.py`

**Arquivo `transicao.csv`**

Esse arquivo deve ser uma tabela de transição de estados para um Autômato Finito Determinístico. A primeira linha da tabela é uma lista dos terminais da gramática, a primeira coluna são todos os possíveis estados que o autômato pode assumir e as transições de estados são os nomes dos próximos estados que o autômato assume ao ler o terminal de sua coluna enquanto no estado de sua linha. Os estados finais válidos devem se iniciar em `qf`. É importante que, para garantir o funcionamento da Análise Léxica, todas as palavras da linguagem terminem no estado `qf1`. Os outros _tokens_, devem ter um estado final cada.
</br> Exemplo (VisuAlg):
![image](https://github.com/VictorPLopes/TradutorUniversal/assets/77900343/e6896116-0344-4d31-a0c9-5d5874ce828c)

**Arquivo `tokens.json`**

Esse arquivo deve mapear os estados finais para _tokens_. O estado `qf1` das palavras reservadas deve ser uma lista com todas as palavras reservadas.
</br> Exemplo (VisuAlg):

```json
{
  "qf1": [
    "algoritmo",
    "inicio",
    "fimalgoritmo",
    "var",
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
    "fimenquanto"
  ],
  "qf2": "var",
  "qf3": "msg",
  "qf4": "valor",
  "qf5": "valor",
  "qf6": "op_arit",
  "qf7": "op_arit",
  "qf8": "compara",
  "qf9": "compara",
  "qf10": "compara",
  "qf11": "atrib",
  "qf12": "(",
  "qf13": ")"
}
```

**Arquivo `pilha.json`**

Esse arqiuvo é a transição do autômato com pilha usado na Análise Sintática. Ele deve ser uma estrutura que mapeia o _token_ da cadeia lida no texto para a lista de variáveis sintáticas que deve ser adicionada à pilha para cada uma das variáveis que podem estar no topo da pilha.
</br> Exemplo (VisuAlg):

```json
{
    "algoritmo": {"S": ["VAR", "COMANDOS"]},
    "inicio": {"VAR": [],
               "DEF_VAR": []},
    "fimalgoritmo": {"COMANDOS":    []},
    "var": {"VAR": ["DEF_VAR"],
            "DEF_VAR": ["TIPO", "DEF_VAR"],
            "NOME_VAR": [],
            "CONTEUDO": [],
            "COMANDOS": ["OP_ATRIB", "ATRIBUICAO", "COMANDOS"],
            "COMANDOS_SE": ["OP_ATRIB", "ATRIBUICAO", "COMANDOS_SE"],
            "COMANDOS_SENAO": ["OP_ATRIB", "ATRIBUICAO", "COMANDOS_SENAO"],
            "COMANDOS_PARA": ["OP_ATRIB", "ATRIBUICAO", "COMANDOS_PARA"],
            "COMANDOS_ENQUANTO": ["OP_ATRIB", "ATRIBUICAO", "COMANDOS_ENQUANTO"],
            "ATRIBUICAO": [],
            "EXPRESSAO": [],
            "COMPARACAO":  ["COMPARA", "VALORES"],
            "VALORES": [],
            "VARIAVEL": []},
    "inteiro": {"TIPO": []},
    "real": {"TIPO": []},
    "logico": {"TIPO": []},
    "caractere": {"TIPO": []},
    "leia": {"COMANDOS": ["ABRE", "NOME_VAR",  "FECHA",  "COMANDOS"],
             "COMANDOS_SE": ["ABRE", "NOME_VAR",  "FECHA",  "COMANDOS_SE"],
             "COMANDOS_SENAO": ["ABRE", "NOME_VAR",  "FECHA",  "COMANDOS_SENAO"],
             "COMANDOS_PARA": ["ABRE", "NOME_VAR",  "FECHA",  "COMANDOS_PARA"],
             "COMANDOS_ENQUANTO": ["ABRE", "NOME_VAR",  "FECHA",  "COMANDOS_ENQUANTO"]},
    "(": {"ABRE": [],
          "ATRIBUICAO": ["EXPRESSAO", "OP_ARIT", "EXPRESSAO", "FECHA"],
          "EXPRESSAO": ["EXPRESSAO", "OP_ARIT", "EXPRESSAO", "FECHA"],
          "COMPARACAO": ["COMPARACAO",  "FECHA", "LOGICO", "ABRE", "COMPARACAO", "FECHA"]},
    ")": {"FECHA": []},
    "escreva": {"COMANDOS": ["ABRE", "CONTEUDO", "FECHA", "COMANDOS"],
                "COMANDOS_SE": ["ABRE", "CONTEUDO", "FECHA", "COMANDOS_SE"],
                "COMANDOS_SENAO": ["ABRE", "CONTEUDO", "FECHA", "COMANDOS_SENAO"],
                "COMANDOS_PARA": ["ABRE", "CONTEUDO", "FECHA", "COMANDOS_PARA"],
                "COMANDOS_ENQUANTO": ["ABRE", "CONTEUDO", "FECHA", "COMANDOS_ENQUANTO"]},
    "msg": {"CONTEUDO": [],
            "ATRIBUICAO": []},
    "atrib": {"OP_ATRIB": []},
    "valor": {"ATRIBUICAO": [],
              "EXPRESSAO": [],
              "VALORES": [],
              "VALOR": []},
    "verdadeiro": {"ATRIBUICAO": [],
                   "VALORES": []},
    "falso": {"ATRIBUICAO": [],
              "VALORES": []},
    "op_arit": {"OP_ARIT": []},
    "se": {"COMANDOS": ["ABRE",  "COMPARACAO",
                        "FECHA",  "ENTAO",
                        "COMANDOS_SE", "COMANDOS"],
           "COMANDOS_SE": ["ABRE",  "COMPARACAO",
                        "FECHA",  "ENTAO",
                        "COMANDOS_SE", "COMANDOS_SE"],
           "COMANDOS_SENAO": ["ABRE",  "COMPARACAO",
                        "FECHA",  "ENTAO",
                        "COMANDOS_SE", "COMANDOS_SENAO"],
           "COMANDOS_PARA": ["ABRE",  "COMPARACAO",
                        "FECHA",  "ENTAO",
                        "COMANDOS_SE", "COMANDOS_PARA"],
           "COMANDOS_ENQUANTO": ["ABRE",  "COMPARACAO",
                        "FECHA",  "ENTAO",
                        "COMANDOS_SE", "COMANDOS_ENQUANTO"]},
    "fimse": {"COMANDOS_SE": [],
              "COMANDOS_SENAO": []},
    "e": {"LOGICO": []},
    "ou": {"LOGICO": []},
    "compara": {"COMPARA": []},
    "entao": {"ENTAO": []},
    "senao": {"COMANDOS_SE": ["COMANDOS_SENAO"]},
    "para": {"COMANDOS": ["VARIAVEL",  "DE", "VALOR",  "ATE",  "VALOR",  "FACA", "COMANDOS_PARA",  "COMANDOS"],
             "COMANDOS_SE": ["VARIAVEL",  "DE", "VALOR",  "ATE",  "VALOR",  "FACA", "COMANDOS_PARA",  "COMANDOS_SE"],
             "COMANDOS_SENAO": ["VARIAVEL",  "DE", "VALOR",  "ATE",  "VALOR",  "FACA", "COMANDOS_PARA",  "COMANDOS_SENAO"],
             "COMANDOS_PARA": ["VARIAVEL",  "DE", "VALOR",  "ATE",  "VALOR",  "FACA", "COMANDOS_PARA",  "COMANDOS_PARA"],
             "COMANDOS_ENQUANTO": ["VARIAVEL",  "DE", "VALOR",  "ATE",  "VALOR",  "FACA", "COMANDOS_PARA",  "COMANDOS_ENQUANTO"]},
    "fimpara": {"COMANDOS_PARA": []},
    "de": {"DE": []},
    "ate": {"ATE": []},
    "faca": {"FACA": []},
    "enquanto": {"COMANDOS": ["ABRE",  "COMPARACAO",  "FECHA",   "FACA",  "COMANDOS_ENQUANTO",  "COMANDOS"],
                 "COMANDOS_SE": ["ABRE",  "COMPARACAO",  "FECHA",   "FACA",  "COMANDOS_ENQUANTO",  "COMANDOS_SE"],
                 "COMANDOS_SENAO": ["ABRE",  "COMPARACAO",  "FECHA",   "FACA",  "COMANDOS_ENQUANTO",  "COMANDOS_SENAO"],
                 "COMANDOS_PARA": ["ABRE",  "COMPARACAO",  "FECHA",   "FACA",  "COMANDOS_ENQUANTO",  "COMANDOS_PARA"],
                 "COMANDOS_ENQUANTO": ["ABRE",  "COMPARACAO",  "FECHA",   "FACA",  "COMANDOS_ENQUANTO",  "COMANDOS_ENQUANTO"]},
    "fimenquanto": {"COMANDOS_ENQUANTO": []}
}
```

**Arquivo `analise_semantica.py`**

A implementação do programa de Análise Semântica depende muito da linguagem desenvolvida. Sua implementação pode ser feita de qualquer forma, desde que, a análise seja feita em uma função chamada `analise_semantica`, que toma como argumento a Tabela de Classificação gerada na Análise Léxica. Essa tabela é uma lista de listas, onde cada entrada é um conjunto `["lexema", "token"]`. O retorno dessa função deve ser uma tupla `(False, "Mensagem de erro")` em caso de erro semântico ou `(True, "Mensagem de sucesso", tabela_variaveis)` em caso de êxito. A `tabela_variaveis` é um dicionário que mapeia o nome de cada variável no código ao seu tipo.
</br> Exemplo (VisuAlg):

```python
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
```

**Arquivo `tradutor.py`**

Assim como o analisador sintático, a implementação do tradutor é livre e dependerá muito das linguagens de origem e destino. A única obrigatoriedade é a função `tradutor`, que toma como argumentos a Tabela de Classificação já citada e a `tabela_variavies` retornada pela etapa sintática. O retorno da função deve ser uma _string_ com o código traduzido.
</br> Exemplo (VisuAlg para C):

```python
em_var = False # variavel que indica se esta dentro de um var
em_atrib = False # variavel que indica se esta dentro de um atribuicao

nivel_indentacao = 0 # variavel que indica o nivel de indentacao atual

dic_tipos = {"inteiro": "int", "real": "float", "caractere": "char", "logico": "int"}

dic_strings = {"inteiro": f"%d", "real": f"%f", "caractere": f"%s", "logico": f"%d"}

def get_indentacao():
    global nivel_indentacao
    return "    " * nivel_indentacao

# Função que traduz o código de VisuAlg para C
def tradutor(tabela_classificacao, tabela_variavies):
    # Variáveis globais
    global em_var, em_atrib, nivel_indentacao
    
    # Variável que armazena o código traduzido
    codigo = ""
    
    i = 0 # Variável que armazena o índice da tabela de classificação
    
    # Para cada palavra na tabela de classificação
    while i < (len(tabela_classificacao)):
        # Se a palavra for algoritmo
        if tabela_classificacao[i][1] == "algoritmo":
            codigo += "#include <stdio.h>\n#include <string.h>\n\n#define TRUE 1\n#define FALSE 0\n\n"
        
        # Se a palavra for var (início da seção de declaracao de variáveis)
        elif tabela_classificacao[i][0] == "var":
            em_var = True
        
        # Se for uma variável
        elif tabela_classificacao[i][1] == "var":
            # Se estiver dentro da seção de declaração de variáveis
            if em_var:
                # Se for do tipo caractere
                if tabela_classificacao[i+1][1] == "caractere":
                    codigo += dic_tipos[tabela_classificacao[i+1][1]] + " " + tabela_classificacao[i][0] + "[100];\n"
                else:
                    codigo += dic_tipos[tabela_classificacao[i+1][1]] + " " + tabela_classificacao[i][0] + ";\n"
                i += 2 # Pula o tipo da variável
                continue
            # Se não estiver dentro da seção de declaração de variáveis
            # Se for uma atribuição
            elif tabela_classificacao[i+1][0] == "=":
                # Se for uma string (mensagem), ignora, pois um strcpy será feito depois ao ler a mensagem
                if tabela_variavies[tabela_classificacao[i][0]] == "caractere":
                    i += 2 # Pula =
                    em_atrib = True
                    continue
                codigo += get_indentacao()
            codigo += tabela_classificacao[i][0] + " "
            # Se tiver finalizado uma atribuição
            if em_atrib and tabela_classificacao[i+1][0] not in ["e", "ou", ")", ">=", "<=", ">", "<", "+", "-", "*", "/", "==", "<>"]:
                codigo += ";\n"
                em_atrib = False
        
        # Se for inicio
        elif tabela_classificacao[i][0] == "inicio":
            codigo += "\nint main() {\n"
            nivel_indentacao += 1
            em_var = False
        
        # Se for leia
        elif tabela_classificacao[i][0] == "leia":
            codigo += get_indentacao() + "scanf(\"" + dic_strings[tabela_variavies[tabela_classificacao[i+2][0]]] + "\", &" + tabela_classificacao[i+2][0] + ");\n"
            i += 4 # Pula (, variavel, )
            continue
        
        # Se for escreva
        elif tabela_classificacao[i][0] == "escreva":
            # Se for uma string (mensagem)
            if tabela_classificacao[i+2][1] == "msg":
                codigo += get_indentacao() + "printf(" + tabela_classificacao[i+2][0] + ");\n"
            # Se for uma variável
            else:
                codigo += get_indentacao() + "printf(\"" + dic_strings[tabela_variavies[tabela_classificacao[i+2][0]]] + "\", " + tabela_classificacao[i+2][0] + ");\n"
            i += 4 # Pula (, variavel, )
            continue
        
        # Se for um = (atribuição)
        elif tabela_classificacao[i][0] == "=":
            codigo += "= "
            em_atrib = True
        
        # Se ler um valor, verdadeiro, falso ou )
        elif tabela_classificacao[i][1] in ["valor", "verdadeiro", "falso", ")"]:
            # Para verdadeiro e falso
            if tabela_classificacao[i][1] == "verdadeiro":
                codigo += "TRUE "
            elif tabela_classificacao[i][1] == "falso":
                codigo += "FALSE "
            else:
                codigo += tabela_classificacao[i][0] + " "
            # Se tiver finalizado uma atribuição
            if em_atrib and tabela_classificacao[i+1][0] not in ["e", "ou", ")", ">=", "<=", ">", "<", "+", "-", "*", "/", "==", "<>"]:
                codigo += ";\n"
                em_atrib = False
                
        # Se ler uma mensagem
        elif tabela_classificacao[i][1] == "msg":
            # Se estiver em uma atribuição, realiza strcpy
            if em_atrib:
                codigo += get_indentacao() + "strcpy(" + tabela_classificacao[i-2][0] + ", " + tabela_classificacao[i][0] + ");\n"
                em_atrib = False
        
        # Se ler um operador <>
        elif tabela_classificacao[i][0] == "<>":
            codigo += "!= "
        
        # Se ler um operador e
        elif tabela_classificacao[i][0] == "e":
            codigo += "&& "
        
        # Se ler um operador ou
        elif tabela_classificacao[i][0] == "ou":
            codigo += "|| "
        
        # Se ler um operador ==, >=, <=, >, <, +, -, *, / ou um (
        elif tabela_classificacao[i][0] in ["==", ">=", "<=", ">", "<", "+", "-", "*", "/", "("]:
            codigo += tabela_classificacao[i][0] + " "
        
        # Se ler um se
        elif tabela_classificacao[i][0] == "se":
            codigo += get_indentacao() + "if "
        
        # Se ler um entao ou um faca
        elif tabela_classificacao[i][0] == "entao" or tabela_classificacao[i][0] == "faca":
            codigo += " {\n"
            nivel_indentacao += 1
        
        # Se ler um senao
        elif tabela_classificacao[i][0] == "senao":
            nivel_indentacao -= 1
            codigo += get_indentacao() + "} else {\n"
            nivel_indentacao += 1
        
        # Se ler um fimse ou um fimpara ou um fimenquanto
        elif tabela_classificacao[i][0] in ["fimse", "fimpara", "fimenquanto"]:
            nivel_indentacao -= 1
            codigo += get_indentacao() + "}\n"
        
        # Se ler um para
        elif tabela_classificacao[i][0] == "para":
            codigo += get_indentacao() + f"for ({tabela_classificacao[i+1][0]} = {tabela_classificacao[i+3][0]}; {tabela_classificacao[i+1][0]} <= {tabela_classificacao[i+5][0]}; {tabela_classificacao[i+1][0]}++) "
            i += 6 # Pula variavel, de, valor, ate e valor
            continue
        
        # Se ler um enquanto
        elif tabela_classificacao[i][0] == "enquanto":
            codigo += get_indentacao() + "while "
        
        # Se ler um fimalgoritmo
        elif tabela_classificacao[i][0] == "fimalgoritmo":
            codigo += get_indentacao() + "return 0;\n}\n"
        
        # Incrementa o índice
        i += 1
    
    # Retorna o código traduzido
    return codigo
```

## Limitações

A principal limitação do programa é que ele só funciona se os lexemas estiverem separados por espaço, e quebra também se houver espaços dentro de um lexema.
