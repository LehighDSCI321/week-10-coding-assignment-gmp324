"""Taking Versatile Digraph Code from week 4, with changes recommended in my feedback"""

class VersatileDigraph:
    """A versatile directed graph supporting node values, weighted edges, and degree utilities."""

    def __init__(self):
        """Initialize an empty directed graph."""
        self.graph = {}          # {from_node: {edge_name: (to_node, weight)}}
        self.node_values = {}    # {node: value}

    def add_node(self, node, value=None):
        """
        Add a node to the graph with an optional value.
        """
        if node not in self.graph:
            self.graph[node] = {}
        self.node_values[node] = value

    def add_edge(self, from_node, to_node, edge_name=None, weight=1):
        """
        Add a directed edge with optional name and weight from one node to another.
        """
        self.add_node(from_node)
        self.add_node(to_node)

        # Generate a unique edge name if none is provided
        if edge_name is None:
            existing_edges = set(self.graph[from_node].keys())
            i = 1
            while f"edge_{i}" in existing_edges:
                i += 1
            edge_name = f"edge_{i}"

        self.graph[from_node][edge_name] = (to_node, weight)

    def get_edge_weight(self, from_node, edge_name):
        """
        Return the weight of a specified edge.
        """
        edge = self.graph.get(from_node, {}).get(edge_name)
        return edge[1] if edge else None

    def update_edge_weight(self, from_node, edge_name, new_weight):
        """
        Update the weight of a specified edge.
        """
        if from_node in self.graph and edge_name in self.graph[from_node]:
            to_node, _ = self.graph[from_node][edge_name]
            self.graph[from_node][edge_name] = (to_node, new_weight)

    def predecessors(self, node):
        """
        Return a list of nodes with edges leading to the given node.
        """
        return [
            u for u, edges in self.graph.items()
            if any(v == node for v, _ in edges.values())
        ]

    def successors(self, node):
        """
        Return a list of nodes that immediately succeed the given node.
        """
        return [v for v, _ in self.graph.get(node, {}).values()]

    def successor_on_edge(self, node, edge_name):
        """
        Return the successor of a node along a given edge.
        """
        edge = self.graph.get(node, {}).get(edge_name)
        return edge[0] if edge else None

    def indegree(self, node):
        """
        Return the number of edges leading into the given node.
        """
        return sum(1 for edges in self.graph.values() for v, _ in edges.values() if v == node)

    def outdegree(self, node):
        """
        Return the number of edges leading out from the given node.
        """
        return len(self.graph.get(node, {}))

    def zero_indegree_nodes(self):
        """Return a list of nodes with zero indegree."""
        return [n for n in self.graph if self.indegree(n) == 0]

    def zero_outdegree_nodes(self):
        """Return a list of nodes with zero outdegree."""
        return [n for n in self.graph if self.outdegree(n) == 0]


class SortableDigraph (VersatileDigraph):
    """A DAG, that supported topological sorting."""

    def top_sort(self):
        """Using Kahn's Algorithm in listing 4-10, perform a topological sort."""
        #initialize in-degree counts first
        count = {u:0 for u in self.graph}

        #count all in-degree...had to fix with iterating .items() per pylint suggestions
        for u, edges in self.graph.items():
            for v, _ in edges.values():
                count[v] += 1

        #collect nodes with in-degree = 0
        Q =[u for u in self.graph if count[u] == 0]
        #empty list for sorted output nodes
        S = []

        #Process nodes in the queue
        while Q:   #while 0-indegree nodes exist
            u = Q.pop()
            S.append(u)
            for v, _ in self.graph[u].values():
                count[v] -= 1  #removing 1 from in-degree counts
                if count[v] == 0: #if node in-degree = 0 it can be start node now
                    Q.append(v)

        #adding this to detect cyclic graphs
        if len(S) != len(self.graph):
            raise ValueError("Graph has a cycle; topological sort not possible.")

        return S