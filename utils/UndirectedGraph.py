class UndirectedGraph:
    def __init__(self):
        self.graph = {}  # Dictionary to store vertices and their edges
        
    def add_vertex(self, vertex):
        """Add a vertex to the graph if it doesn't exist."""
        if vertex not in self.graph:
            self.graph[vertex] = set()
    
    def add_edge(self, vertex1, vertex2):
        """Add an undirected edge between vertex1 and vertex2."""
        # Add vertices if they don't exist
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        # Add edges in both directions
        self.graph[vertex1].add(vertex2)
        self.graph[vertex2].add(vertex1)
    
    def remove_edge(self, vertex1, vertex2):
        """Remove the edge between vertex1 and vertex2."""
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].discard(vertex2)
            self.graph[vertex2].discard(vertex1)
    
    def remove_vertex(self, vertex):
        """Remove a vertex and all its edges from the graph."""
        if vertex in self.graph:
            # Remove all edges containing this vertex
            for neighbor in self.graph[vertex]:
                self.graph[neighbor].discard(vertex)
            # Remove the vertex
            del self.graph[vertex]
    
    def get_vertices(self):
        """Return all vertices in the graph."""
        return list(self.graph.keys())
    
    def get_edges(self):
        """Return all edges in the graph as a list of tuples."""
        edges = set()
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                # Sort the vertices to ensure we don't add the same edge twice
                edge = tuple(sorted([vertex, neighbor]))
                edges.add(edge)
        return list(edges)
    
    def get_neighbors(self, vertex):
        """Return all neighbors of a vertex."""
        if vertex in self.graph:
            return list(self.graph[vertex])
        return []
    
    def has_edge(self, vertex1, vertex2):
        """Check if an edge exists between vertex1 and vertex2."""
        return vertex1 in self.graph and vertex2 in self.graph[vertex1]
    
    def degree(self, vertex):
        """Return the degree of a vertex (number of edges connected to it)."""
        if vertex in self.graph:
            return len(self.graph[vertex])
        return 0
    
    def __str__(self):
        """Return a string representation of the graph."""
        return f"Vertices: {self.get_vertices()}\nEdges: {self.get_edges()}"