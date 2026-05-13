import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.getAllEdges()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)

        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight = t.peso)
