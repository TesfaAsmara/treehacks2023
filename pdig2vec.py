from node2vec import Node2Vec

class ProbDig2Vec(Node2Vec):
  """
  Node2Vec with added backward edges and backward discount
  The weights on the original edges would be `backward_prob` times
  greater than the weights on the ghost backward edges
  """
  def __init__(self, graph, backward_prob=0.1, **kwargs):
    self.backward_prob = backward_prob
    graph = self._add_backward_edges(graph)
    super().__init__(graph, **kwargs)

  def _add_backward_edges(self, graph):
    edges = set(graph.edges)
    for x, y in edges:
      graph[x][y]["weight"] = 1 - self.backward_prob
    for x, y in edges:
      if (y,x) in edges:
        graph[y][x]["weight"] += self.backward_prob
      else:
        graph.add_edge(y, x, weight=self.backward_prob)
    edges = set(graph.edges)
    for x, y in edges:
      if graph[x][y]["weight"] == 0:
        graph.remove_edge(x, y)
    return graph

  def get_embeddings(self, window=1, silent=False):
    self.window = window
    if not silent:
      self.print_parameters()
    model = self.fit(window=1)
    num_nodes = self.graph.number_of_nodes()
    emb = model.wv[[str(i) for i in range(num_nodes)]]
    return emb

  def print_parameters(self):
    print(f"backward_prob = {self.backward_prob}, dimension = {self.dimensions}, walk_length = {self.walk_length}, num_walks = {self.num_walks}, window = {self.window}")