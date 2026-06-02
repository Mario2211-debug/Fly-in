from collections import deque
import heapq

# Labirinto: E = entrada, S = saída, # = parede, . = caminho
labirinto = [
    "E..#....",
    "..#.#...",
    "....#...",
    "#.##....",
    ".....#..",
    ".....#.S"
]


def encontra_posicoes(labirinto):
    """Encontra entrada (E) e saída (S)"""
    inicio = fim = None
    for i, linha in enumerate(labirinto):
        for j, char in enumerate(linha):
            if char == 'E':
                inicio = (i, j)
            elif char == 'S':
                fim = (i, j)
    return inicio, fim


def vizinhos(pos, labirinto):
    """Retorna vizinhos válidos (cima, baixo, esquerda, direita)"""
    i, j = pos
    moves = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    validos = []

    for x, y in moves:
        if 0 <= x < len(labirinto) and 0 <= y < len(labirinto[0]):
            if labirinto[x][y] != '#':
                validos.append((x, y))
    return validos


def bfs(labirinto, inicio, fim):
    """Busca em Largura - Fila"""
    print("\n=== BFS (Busca em Largura) ===")
    fila = deque([inicio])
    visitados = {inicio}
    pai = {inicio: None}

    passos = 0
    while fila:
        passos += 1
        atual = fila.popleft()
        print(f"Passo {passos}: Visitando {atual}")

        if atual == fim:
            print(f"✓ Encontrado! Passos totais: {passos}")
            return reconstruir_caminho(pai, inicio, fim)

        for viz in vizinhos(atual, labirinto):
            if viz not in visitados:
                visitados.add(viz)
                pai[viz] = atual
                fila.append(viz)

    print("✗ Caminho não encontrado")
    return None


def dfs(labirinto, inicio, fim):
    """Busca em Profundidade - Pilha"""
    print("\n=== DFS (Busca em Profundidade) ===")
    pilha = [inicio]
    visitados = {inicio}
    pai = {inicio: None}

    passos = 0
    while pilha:
        passos += 1
        atual = pilha.pop()
        print(f"Passo {passos}: Visitando {atual}")

        if atual == fim:
            print(f"✓ Encontrado! Passos totais: {passos}")
            return reconstruir_caminho(pai, inicio, fim)

        for viz in vizinhos(atual, labirinto):
            if viz not in visitados:
                visitados.add(viz)
                pai[viz] = atual
                pilha.append(viz)

    print("✗ Caminho não encontrado")
    return None


def distancia_manhattan(pos, fim):
    """Heurística para A*: distância em linha reta (ignorando paredes)"""
    return abs(pos[0] - fim[0]) + abs(pos[1] - fim[1])


def a_star(labirinto, inicio, fim):
    """Algoritmo A* - Fila de Prioridade"""
    print("\n=== A* (A-estrela) ===")

    # heap = (custo_f, contador, posicao)
    # contador serve para desempate na heap
    contador = 0
    heap = [(distancia_manhattan(inicio, fim), contador, inicio)]

    custo_g = {inicio: 0}
    custo_f = {inicio: distancia_manhattan(inicio, fim)}
    pai = {inicio: None}
    visitados = set()

    passos = 0
    while heap:
        passos += 1
        f_atual, _, atual = heapq.heappop(heap)

        if atual in visitados:
            continue

        visitados.add(atual)
        print(f"Passo {passos}: Visitando {atual} (f={f_atual:.0f})")

        if atual == fim:
            print(f"✓ Encontrado! Passos totais: {passos}")
            return reconstruir_caminho(pai, inicio, fim)

        for viz in vizinhos(atual, labirinto):
            if viz in visitados:
                continue

            g_tentativo = custo_g[atual] + 1

            if viz not in custo_g or g_tentativo < custo_g[viz]:
                pai[viz] = atual
                custo_g[viz] = g_tentativo
                h = distancia_manhattan(viz, fim)
                custo_f[viz] = g_tentativo + h
                contador += 1
                heapq.heappush(heap, (custo_f[viz], contador, viz))

    print("✗ Caminho não encontrado")
    return None


def reconstruir_caminho(pai, inicio, fim):
    """Reconstrói o caminho do início ao fim"""
    caminho = []
    atual = fim
    while atual != inicio:
        caminho.append(atual)
        atual = pai[atual]
    caminho.append(inicio)
    caminho.reverse()

    print(f"\nCaminho encontrado: {caminho}")
    print(f"Tamanho do caminho: {len(caminho)} passos")
    return caminho


def mostrar_labirinto_com_caminho(labirinto, caminho):
    """Mostra o labirinto com o caminho marcado como *"""
    if not caminho:
        return

    # Converte para lista de listas para modificar
    lab = [list(linha) for linha in labirinto]

    for i, j in caminho:
        if lab[i][j] not in ['E', 'S']:
            lab[i][j] = '*'

    print("\nLabirinto com caminho:")
    for linha in lab:
        print(''.join(linha))


# Execução principal
if __name__ == "__main__":
    inicio, fim = encontra_posicoes(labirinto)

    print("Labirinto original:")
    for linha in labirinto:
        print(linha)

    print(f"\nEntrada: {inicio}")
    print(f"Saída: {fim}")

    # Testa os três algoritmos
    print("\n" + "="*50)

    caminho_bfs = bfs(labirinto, inicio, fim)
    mostrar_labirinto_com_caminho(labirinto, caminho_bfs)

    print("\n" + "="*50)

    caminho_dfs = dfs(labirinto, inicio, fim)
    mostrar_labirinto_com_caminho(labirinto, caminho_dfs)

    print("\n" + "="*50)

    caminho_a = a_star(labirinto, inicio, fim)
    mostrar_labirinto_com_caminho(labirinto, caminho_a)
