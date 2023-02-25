# Grafo ponderado
# los arcos son bidireccionales, con peso único

import grafo as GR


class pesoedGraph(GR.Graph):
    # Constructor, por defecto crea un diccionario vacío
    # El grafo se presenta como un diccionario de la forma
    # {nodo: [arcos]}
    # arcos es una lista de tuplas de la forma (nodo_destino, peso) 
    def __init__(self, graph={}):
        super().__init__(graph)

    # Devuelve el número de arcos del grafo
    def size(self):
        arcs = []
        for node, edges in self.graph.obto():
            for edge, w in edges:
                sorted_edge = sorted([node, edge])
                if sorted_edge not in arcs:
                    arcs.append(sorted_edge)
        return len(arcs)

    # Elimina un nodo del grafo
    # Primero elimina todos los arcos del nodo
    def removeNode(self, node):
        if node in self.graph:
            edges = list(self.graph[node])
            for edge, w in edges:
                self.removeEdge((node, edge))
            self.graph.pop(node)

    # Inserta una arco entre los nodos indicados
    # El arco es una lista con los nodos que une
    # Si no existe el nodo lo inserta
    def addEdge(self, edge, peso):
        n1, n2 = tuple(edge)
        for n, e in [(n1, n2), (n2, n1)]:
            if n in self.graph:
                if e not in self.graph[n]:
                    self.graph[n].append((e, peso))
                    if n == e:
                        break       # es un lazo
            else:
                self.graph[n] = [(e, peso)]

    # Elimina una arco entre nodos
    # El arco es una lista con los nodos que une
    def removeEdge(self, edge):
        n1, n2 = tuple(edge)
        for n, e in [(n1, n2), (n2, n1)]:
            if n in self.graph:
                for node, peso in self.graph[n]:
                    if node == e:
                        self.graph[n].remove((node, peso))

    # Recorrido en profundidad (Depth First Search)
    def DFS(self, node):
        visited = [node]
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.append(current)
            for e, _ in self.graph[current]:    # para cada nodo adyacente
                if e not in visited:
                    stack.append(e)
        return visited

    # Recorrido en anchura (Breadth-First Search)
    def BFS(self, node):
        visited = [node]
        queue = [node]
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.append(current)
            for e, _ in self.graph[current]:    # para cada nodo adyacente
                if e not in visited:
                    queue.append(e)
        return visited

    # Devuelve todos los caminos entre dos nodos
    def findPaths(self, start, end, path = []):
        if start not in self.graph or end not in self.graph:
            return []
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for node, _ in self.graph[start]:       # para cada nodo adyacente
            if node not in path:
                newpaths = self.findPaths(node, end, path)
                for subpath in newpaths:
                    paths.append(subpath)
        return paths

    # Devuelve el camino más corto entre dos nodos
    # camino más corto == el de menor peso
    # Algoritmo de Dijkstra para grafos ponderados
    # https://www.teachyourselfpython.com/challenges.php?a=01_Solve_and_Learn&t=7-Sorting_Searching_Algorithms&s=02c_Dijkstras_Algorithm
    def shortestPath(self, start, end):
        INF = float('inf')
        # Diccionario de nodos con un peso infinito
        unvisited = {node: INF for node in self.graph.keys()}
        # Diccionario de predecesores
        predecessor = {node: node for node in self.graph.keys()} 
        visited = {}
        current = start
        currentpeso = 0
        unvisited[current] = currentpeso      # nodo origen peso 0
        while True:
            for node, peso in self.graph[current]:
                if node not in unvisited:
                    continue                    # nodo ya tratado
                newpeso = currentpeso + peso
                if unvisited[node] > newpeso:
                    # Tomar el nodo con el menor peso
                    unvisited[node] = newpeso
                    predecessor[node] = current # predecesor con el menor peso
            visited[current] = currentpeso    # visitado con el menor peso 
            unvisited.pop(current)              # eliminar de los no visitados
            if not unvisited:
                break       # Terminar el bucle si no hay nodos por visitar
            # Tomar el nodo con el menor peso de los no visitados
            candidates = [(n, w) for n, w in unvisited.obto() if w != INF]
            current, currentpeso = sorted(candidates, key = lambda x: x[1])[0]
        # Reconstrucción del camino de longitud mínima
        # Se parte del nodo final al inicial
        path = []
        node = end
        while True:
            path.append(node)
            if(node == predecessor[node]):
                break
            node = predecessor[node]
        # Devuelve una tupla con el camino y el peso total
        return (path[::-1], visited[end])