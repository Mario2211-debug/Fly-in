from inout.parser import parser
from core.drones import Drones
from utils.algorithms import dijkstra
from utils.render import Renderer


def app():
    file = open("./maps/challenger/01_the_impossible_dream.txt", "r")
    config = parser(file)
    graph = config.build_graph()


# inicializa mlx, cria janela e imagem com win_w, win_h
# ...

    caminho, custo = dijkstra(graph, (config.start.x, config.start.y),
                              (config.end.x, config.end.y), config)
    print(f"Melhor caminho: {caminho} com custo {custo}")
    drones = Drones(config.n_drones, caminho, config)
    drones.run()
    renderer = Renderer(config)
    renderer.run()
