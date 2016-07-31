# Graph data structure

class Graph():

    edge_list = 0
    def __init__(self, n):
        self.graph_size= n
        self.edge_list ={}
        self.edge_cnt = 0
        for x in range(1,n+1):
            self.edge_list[x]=set()


    def add_edge(self, a, b):
        if a > self.order():
            print "Can not add edge because", a, "is not a vetex in the graph."
        elif b > self.order():
            print "Can not add edge because", b, "is not a vetex in the graph."
        elif a != b:
            self.edge_list[a].add(b)
            self.edge_list[b].add(a)
            self.edge_cnt=self.edge_cnt+1
            print "edge between",a,"and",b,"added"

    def print_graph(self):
        if self.is_empty():
            print "Graph is empty!"
        else:
            for j in range(1, self.order()+1):
                if self.edge_list[j]:
                    print j, ":", self.edge_list[j]

    def clear(self):
        for j in range(1, self.order()+1): #to clear sets (edges)
            self.edge_list[j].clear()
        self.edge_cnt=0

    def order(self):
        return len(self.edge_list)  #returns the number of vertices in the graph

    def size(self):
        return self.edge_cnt #returns the number of edges in the graph

    def remove_edge(self, a, b): #removes an edge
        if b in self.edge_list[a]:
            self.edge_list[a].remove(b)
            self.edge_list[b].remove(a)
            self.edge_cnt= self.edge_cnt-1

    def is_empty(self):
        if self.edge_cnt!=0:
            return False
        return True

    def is_complete(self):
        if self.edge_cnt==0:
            return False
        return True

g = Graph(10)
g.add_edge(1,2)
g.add_edge(1,3)
g.print_graph()
g.add_edge(11,1)
g.is_empty()
g.is_complete()
