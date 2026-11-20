import json,pickle,networkx as nx,time
from networkx.algorithms.isomorphism import GraphMatcher
edges=json.load(open('../../data/edges.json'))
G=nx.Graph(); G.add_nodes_from(range(56)); G.add_edges_from(edges)
t=time.time(); auts=[]
for m in GraphMatcher(G,G).isomorphisms_iter():
    auts.append(tuple(m[i] for i in range(56)))
    if len(auts)>=200000 or time.time()-t>400: break
print(len(auts),time.time()-t)
pickle.dump(auts,open('auts.pkl','wb'))
