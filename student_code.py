"""TraversableDigraph and DAG implementations, extending SortableDigraph."""
from collections import deque #for queue structure bfs
from SortableDigraph import SortableDigraph

class TraversableDigraph(SortableDigraph):
    """Augments SortableDigraph with BFS and DFS methods."""

    def add_node(self, node, value=None):
        """Add a node with an optional value."""
        super().add_node(node, value)

    def get_nodes(self):
        """Return a list of nodes in the graph."""
        return list(self.graph.keys())

    def get_node_value(self, node):
        """Return the value associated with a node."""
        return self.node_values.get(node, None)

    def dfs(self, start):
        """Depth-First Search...based on Listing 5-5 from Python Algs."""
        visited, stack = set(), [start]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            stack.extend(v for v, _ in self.graph.get(u, {}).values())
            yield u

    def bfs(self, start):
        """Breadth-First Search...based on Listing 5-6 from Python Algs."""
        visited, queue = set(), deque([start])
        while queue:
            u = queue.popleft()
            if u in visited:
                continue
            visited.add(u)
            for v, _ in self.graph.get(u, {}).values():
                queue.append(v)
            yield u

class DAG(TraversableDigraph):
    """DAG...to prevent graph cycles"""

    def add_edge(self, u, v, edge_name=None, weight=1, **kwargs):
        """adds edge from u to v, if a cycle is not created"""
        if self._path_exists(v, u):
            raise ValueError(f"Adding edge {u} -> {v} creates a cycle.")
        super().add_edge(u, v, edge_name=edge_name, weight=weight)

    def _path_exists(self, start, target):
        """helper method to return true if target is reachable from start"""
        for node in self.dfs(start):
            if node == target:
                return True
        return False
