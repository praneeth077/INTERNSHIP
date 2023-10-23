import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('AI2Peat_Relationship.csv', delimiter=';')
G = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source = 'Paper_Number_Cited', target = 'Paper_Number_Quoter')

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size = 2)
nx.draw_networkx_edges(G, pos, width = 0.5)
nx.draw_networkx_labels(G, pos, font_size = 1)

ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()