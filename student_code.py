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
    """"""


    pass

