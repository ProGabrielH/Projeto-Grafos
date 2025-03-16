import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def criar_grafo(arquivo_csv):
    colunas = ["airline", "airline_id", "source", "source_id", "destination", "destination_id", "codeshare", "stops",
               "equipment"]
    df = pd.read_csv(arquivo_csv, names=colunas)

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row["source"], row["destination"], airline=row["airline"], stops=int(row["stops"]))

    return G


def analisar_centralidade(G):
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    total_degree = {node: in_degree[node] + out_degree[node] for node in G.nodes()}

    top_airports = sorted(total_degree.items(), key=lambda x: x[1], reverse=True)[:10]

    print("\nTop 10 aeroportos mais conectados:")
    for airport, degree in top_airports:
        print(f"{airport}: {degree} conexões")

    plt.figure(figsize=(10, 6))
    subgraph = G.subgraph([airport for airport, _ in top_airports])
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True,
            node_size=[v * 100 for v in total_degree.values() if v in dict(top_airports).values()], font_size=10)
    plt.show()


def simular_falha(G, aeroportos_removidos):
    G_modificado = G.copy()

    G_modificado.remove_nodes_from(aeroportos_removidos)

    num_ilhas = nx.number_weakly_connected_components(G_modificado)

    print("\nSIMULAÇÃO DE FALHA NA REDE AÉREA")
    print(f"Aeroportos removidos: {aeroportos_removidos}")
    print(f"Total de aeroportos antes: {len(G.nodes)}")
    print(f"Total de aeroportos depois: {len(G_modificado.nodes)}")
    print(f"Número de ilhas formadas: {num_ilhas}")

    visualizar_grafo_completo(G_modificado)

    return G_modificado


def visualizar_grafo_completo(G):
    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G, k=0.3)  # Ajusta o espaçamento dos nós
    nx.draw(
        G, pos, with_labels=True, node_size=500, font_size=10, edge_color="gray", alpha=0.5
    )

    plt.title("Grafo Completo das Rotas Aéreas")
    plt.show()


if __name__ == "__main__":
    arquivo_csv = "AirlinesDB.csv"
    G = criar_grafo(arquivo_csv)

    print(f"Número de aeroportos: {G.number_of_nodes()}")
    print(f"Número de rotas: {G.number_of_edges()}")

    # analisar_centralidade(G)  # Mostra os hubs principais
    # visualizar_grafo_completo(G)  # Mostra o grafo inteiro
    # falha = simular_falha(G, ["GRU", "VCP"]) # Análise de falha
