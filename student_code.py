"""TraversableDigraph and DAG implementations, extending SortableDigraph."""
from collections import deque #for queue structure bfs
from SortableDigraph import SortableDigraph

class TraversableDigraph(SortableDigraph):
    """Augments SortableDigraph with BFS and DFS methods."""

    def get_nodes(self):
        """Return a list of nodes in the graph."""
        return list(self.graph.keys())

    def get_node_value(self, node):
        """Return the value stored for a node, or None if not set."""
        return self.node_values.get(node, None)

    def dfs(self, start):
        """Depth-First Search excluding the start node."""
        visited, stack = set([start]), [start]
        while stack:
            u = stack.pop()
            for v, _ in self.graph.get(u, {}).values():
                if v not in visited:
                    visited.add(v)
                    stack.append(v)
                    yield v


    def bfs(self, start):
        """Breadth-First Search...based on Listing 5-6 from Python Algorithms."""
        visited, queue = set(), deque([start])
        visited.add(start)
        while queue:
            u = queue.popleft()
            for v, _ in self.graph.get(u, {}).values():
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
                    yield v


class DAG(TraversableDigraph):
    """DAG that prevents cycles when adding edges."""

    def add_edge(self, u, v, edge_name=None, edge_weight=1, **kwargs):
        """Add edge from u to v if no cycle is created."""
        if self._path_exists(v, u):
            raise ValueError(f"Adding edge {u} -> {v} creates a cycle.")
        super().add_edge(u, v, edge_name=edge_name, weight=edge_weight)


    def _path_exists(self, start, target):
        """Return True if target is reachable from start."""
        for node in self.dfs(start):
            if node == target:
                return True
        return False
