#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" nqueens.py
Referências consultadas:
 - Livro AIMA - "Artificial Intelligence - A Modern Approach"
 - Github oficial do livro AIMA (https://github.com/aimacode)
 - Documentação do Python (https://docs.python.org)"""


def ler_entrada():
    """ Lê dois parâmetros em linha de comando:
    - n: tamanho do tabuleiro /  numero de rainhas
    - metodobusca: bfs (busca em largura) ou dfs (busca em profundidade) """
    while True:
        try:
            entrada = input()
            n = int(entrada.split()[0])
            metodobusca = str(entrada.split()[1])
            if validar_entrada(n, metodobusca):
                break
        except Exception as erro:
            print(f"Erro: {erro}")
    return n, metodobusca


def validar_entrada(n, metodobusca):
    """ Valida os dois parâmetros em linha de comando:
    n: numero inteiro maior ou igual a 4
    metodobusca: string "bfs" (busca em largura) ou "dfs" (busca em profundidade) """
    if n < 4:
        print("Erro: O número n deve ser maior ou igual a 4.")
        return False
    if metodobusca not in ["dfs", "bfs"]:
        print("Erro: O tipo de busca deve ser bfs ou dfs.")
        return False
    return True


def testar_objetivo(vetor_resposta):
    """ Retorna True se todas as colunas do vetor estão preenchidas corretamente e sem conflitos. """
    if vetor_resposta[-1] is -1:
        return False
    return not any(em_conflito(vetor_resposta, vetor_resposta[coluna], coluna)
                for coluna in range(len(vetor_resposta)))


def em_conflito(vetor_resposta, linha, coluna):
    """ retorna True se existe pelo menos uma rainha em (linha, coluna) em conflito com as demais. """
    return any(checar_conflito(linha, coluna, vetor_resposta[c], c)
            for c in range(coluna))


def checar_conflito(linha1, coluna1, linha2, coluna2):
    """ Checa conflito entre duas rainhas localizadas em (linha1, coluna1) e (linha2, coluna2). """
    return (linha1 == linha2 or  # mesma linha
            coluna1 == coluna2 or  # mesma coluna
            linha1 + coluna1 == linha2 + coluna2 or  # mesma diagonal principal
            linha1 - coluna1 == linha2 - coluna2)    # mesma diagonal secundária


def definir_posicoes_possiveis(vetor_resposta):
    """ Na primeira coluna não resolvida à esquerda que encontrar, analisa e retorna as linhas que nao causam conflito."""
    if vetor_resposta[-1] is not -1:
        return []  # todas as colunas já estão preenchidas;
    else:
        coluna = vetor_resposta.index(-1)  # retorna a posição em que está o próximo -1.
        return [linha for linha in range(len(vetor_resposta))
                if not em_conflito(vetor_resposta, linha, coluna)]  # retorna linhas possíveis para a rainha


def atualizar_vetor(vetor_resposta, linhaescolhida):
    """Coloca a rainha na posição."""
    coluna = vetor_resposta.index(-1)
    novo_vetor_resposta = vetor_resposta[:]
    novo_vetor_resposta[coluna] = linhaescolhida
    return novo_vetor_resposta


class No:
    """ Classe das possíveis soluções. Contém um caminho para o pai e o vetor_resposta atualizado na linha escolhida. """
    def __init__(self, vetor_resposta, pai=None, linhaescolhida=None):
        """Cria uma árvore de busca, derivada de um pai e uma ação."""
        self.vetor_resposta = vetor_resposta
        self.pai = pai
        self.linhaescolhida = linhaescolhida

    def expandir(self, no):
        """Geração de nós com vetor_respostaes corretos possíveis para a próxima coluna."""
        return [self.no_filho(no, linhaescolhida)
                for linhaescolhida in definir_posicoes_possiveis(self.vetor_resposta)]

    def no_filho(self, no, linhaescolhida):
        """ Cria o proximo no. """
        vetor_resposta_atualizado = atualizar_vetor(self.vetor_resposta, linhaescolhida)
        proximo_no = No(vetor_resposta_atualizado, self, linhaescolhida)
        return proximo_no

    def solucao(self):
        """Returna a sequência de posições das linhas escolhidas da primeira solução encontrada,
        somando 1 em todas as posições para compatibilizar posição inicial em 1."""
        return [no.linhaescolhida+1 for no in self.caminho()[1:]]

    def caminho(self):
        """Retorna uma lista de nós que forma o caminho da raiz a até o nó."""
        no, caminho_de_volta = self, []
        while no:
            caminho_de_volta.append(no)
            no = no.pai
        return list(reversed(caminho_de_volta))


def main():
    """ Programa Principal. """
    n, metodobusca = ler_entrada()
    fronteira = [No([-1] * n)]  # cria um nó com um vetor_resposta com -1 nas n posições.

    while fronteira:
        # Método: Se é busca em profundidade usa pilha, se é em largura usa fila.
        if metodobusca == "dfs":
            no = fronteira.pop(-1)
        if metodobusca == "bfs":
            no = fronteira.pop(0)

        # Imprime e retorna a primeira solução encontrada, caso contrário expande o nó.
        if testar_objetivo(no.vetor_resposta):
            return print(*no.solucao())
        else:
            fronteira.extend(no.expandir(no))


if __name__ == '__main__':
    main()