"""Creating TraversableDigraph and DAG classes with some inheritance dependencies"""
from SortableDigraph import SortableDigraph #for inheritance
from collections import deque #for queue structure in bfs

class TraversableDigraph(SortableDigraph):
    """augments SortableDigraph with BFS and DFS methods"""

    def dfs(self, start):
        """Depth-First Search...based on Listiing 5-5 from Python Algs."""
        visited, stack = set(), [start] #visited and set queue
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            stack.extend(self.graph.get(u, []))
            yield u

    def bfs(self, start):
        """Breadth-First Search...based on Listing 5-6 from Python Algs."""
        visited, queue=set(), deque([start])
        while queue:
            u = u.queue.popleft()
            if u in visited:
                continue
            visited.add(u)
            for v in self.graph.get(u, []):
                queue.append(v)
            yield u

class DAG(TraversableDigraph):
    """DAG...to prevent graph cycles"""

    def add_edge(self, u,v):
        """adds edge from u to v, if a cycle is not created"""
        if self._path_exists(v,u):
            raise ValueError(f"Adding edge {u} -> {v} creates a cycle.")
        super().add_edge(u, v)

    def _path_exists(self, start, target):
        """helper method to return true if target is reachable from start"""
        for node in self.dfs(start):
            if node == target:
                return True
        return False
