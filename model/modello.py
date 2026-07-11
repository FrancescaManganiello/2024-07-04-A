from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()  # un grafo orientato e non pesato
        self._nodes = []
        self._idMap = {}
        self._edges = []

    # PUNTO 1a ----------------------------------------------------------
    def getYears(self):
        return DAO.getAllYears()
    # FINE PUNTO 1a ----------------------------------------------------------

    # PUNTO 1b ----------------------------------------------------------
    def getShapesYear(self, year):
        return DAO.getShapesYear(year)
    # FINE PUNTO 1b ----------------------------------------------------------

    # PUNTO 1c ----------------------------------------------------------
    def buildGraph(self, anno, forma):
        self._graph.clear()
        self._idMap.clear()
        self._nodes = DAO.getAllNodes(anno, forma)
        for n in self._nodes:
            self._idMap[n.id] = n

        self._graph.add_nodes_from(self._nodes)

        self._edges = DAO.getAllEdges(anno, forma)
        for a1, a2 in self._edges:
            if a1 in self._idMap and a2 in self._idMap:
                self._graph.add_edge(self._idMap[a1], self._idMap[a2])
    # FINE PUNTO 1c ----------------------------------------------------------

    # PUNTO 1d ----------------------------------------------------------
    # Stampare il numero di componenti debolmente connesse.
    def get_num_connesse(self):
        return nx.number_weakly_connected_components(self._graph)

    #  identificare la componente connessa di dimensione maggiore, e stamparne i nodi.
    def getConnectedComponents(self):

        conn = list(nx.weakly_connected_components(self._graph))
        conn.sort(key=lambda x: len(x), reverse=True)

        return conn[0]
    # FINE PUNTO 1d ----------------------------------------------------------

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())
