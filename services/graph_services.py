import networkx as nx
import matplotlib.pyplot as plt


def create_graph(dataframe):
    city_graph = nx.from_pandas_edgelist(dataframe, 'from_station_id', 'to_station_id')
    nx.draw(city_graph, with_labels=False)
    plt.savefig("filename.png")