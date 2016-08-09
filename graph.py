import random
import collections
import igraph
import operator
from operator import itemgetter
class Graph():
    # edge_list = 0 (Do we need this?)
    def __init__(self, n):
        self.graph_size = n
        self.edge_list = {}      # a dictionary whose keys are the vertices and the values are the set of adjacent vertices
        self.edge_cnt = 0        # number of edges
        self.vertex_colour = {}
        self.vertex_degree = {}
        for x in range(1, n+1):
            self.edge_list[x] = set()
            self.vertex_colour[x] = 0

    def add_edge(self, a, b):
        """ Add edge between the vertices a and b to graph"""
        if a > self.order():
            print ("Can not add edge because", a, "is not a vetex in the graph.")
        elif b > self.order():
            print ("Can not add edge because", b, "is not a vetex in the graph.")
        elif a != b:
            self.edge_list[a].add(b)
            self.edge_list[b].add(a)
            self.edge_cnt=self.edge_cnt+1
            # print ("edge between",a,"and",b,"added")

    def print_graph(self):
        if self.is_empty():
            print ("Graph is empty!")
        else:
            for j in range(1, self.graph_size +1):
                    print ("vertex",j, "neighbours", self.edge_list[j],"colour",self.vertex_colour[j])

    def clear(self):
        for j in range(1, self.order()+1):  #to clear sets (edges)
            self.edge_list[j].clear()
        self.edge_cnt=0

    def order(self):
        return len(self.edge_list)       #returns the number of vertices in the graph

    def size(self):
        return self.edge_cnt               #returns the number of edges in the graph

    def remove_edge(self, a, b):           #removes an edge
        if b in self.edge_list[a]:
            self.edge_list[a].remove(b)
            self.edge_list[b].remove(a)
            self.edge_cnt= self.edge_cnt-1

    def is_empty(self):
        if self.edge_cnt!=0:
            return False
        return True

    def is_complete(self):
        if self.edge_cnt==self.order()*(self.order()-1)/2:
            return True
        return False

    #def naive_colouring(self):
        #### random colours but can have duplicates
        #for k in range(1, self.order() + 1):
            #self.vertex_colour[k]=random.randint(0, self.order())

        #### vertex colour is added in order from 1 to vertex's number then values are shuffled (no duplicate colours)
        # for k in range(1, self.order() + 1):
        #     self.vertex_colour[k] = k
        # values = list( )
        # random.shuffle(values)
        # self.vertex_colour= dict(zip(self.vertex_colour.keys(), values))
        # print (self.vertex_colour)

    def colour_count(self):
        if self.vertex_colour[1] == 0:
            return 0
        else:
            colour_set = set(self.vertex_colour.values()) # colours are a set to remove duplicates, then it gets the len
            return (len(colour_set))


    def degree_lowest(self):
        """arranges a dict of vertices and edges starting from the lowest degree"""
        vertex_degree={}
        for v in range(1, self.order() + 1):
            vertex_degree[v] = len(self.edge_list[v])
        sorted_degree = sorted(vertex_degree.items(), key=operator.itemgetter(1))
        order_lowest = []
        for a, b in sorted_degree:
            order_lowest.append(a)
        return order_lowest

    def degree_highest(self):
        l = self.degree_lowest()
        l.reverse()
        return l

    def greedy_algo(self,order_deg):
        for x in range(1,self.graph_size +1):
            self.vertex_colour[x]=0
        if order_deg == "l":
            v = self.degree_lowest()
        elif order_deg == "h":
            v = self.degree_highest()
        for j in range(0, len(v)):
            nb = list(self.edge_list[v[j]])  # place the neighbours in a list
            colour = {}  # empty colour dict
            for i in range(1, self.graph_size + 1):  # loop to set all colours to be available
                colour[i] = True
            # loop checks if all the vertex neighbours have a colour, if they do, the colour is “false” (unavailable)
            for x in nb:
                nb_colour = self.vertex_colour[x]
                if nb_colour != 0:  # if the neighbour has a colour
                    colour[nb_colour] = False
                    # change the colour to be not available
                    # loop to find the first available colour so we will loop till we find the first true
            for i in range(1, len(colour) + 1):  # find the first available colour
                if colour[i] is True:
                    self.vertex_colour[v[j]] = i
                    break

    def random_graph(self، p):
        self.clear()
        for v1 in range(1, self.graph_size + 1):
            for v2 in range(v1, self.graph_size + 1):
                if v1 != v2 and random.random() < p:
                    self.add_edge(v1,v2)


    def greedy_algo2(self):
        """colours graph using the greedy algorithm"""
        for x in range(1,self.graph_size +1):
            self.vertex_colour[x]=0
        for v in range(1, self.order() + 1):
            nb = list(self.edge_list[v])  # place the neighbours in a list
            colour = {}  # empty colour dict
            for i in range(1, self.order() + 1):  # loop to set all colours to be available
                colour[i] = True
            # loop checks if all the vertex neighbours have a colour, if they do, the colour is “false” (unavailable)
            for x in nb:
                nb_colour = self.vertex_colour[x]
                if nb_colour != 0:  # if the neighbour has a colour
                    colour[nb_colour] = False
                    # change the colour to be not available
                    # loop to find the first available colour so we will loop till we find the first true
            for i in range(1, len(colour) + 1):  # find the first available colour
                if colour[i] is True:
                    self.vertex_colour[v] = i
                    break
    #
    # def draw(self):
    #     g = igraph.Graph()
    #     g.add_vertices(self.order())
    #     for v in range(1, self.order() + 1):
    #         for w in range(v + 1, self.order() + 1):
    #             if w in self.edge_list[v]:
    #                 g.add_edge(v - 1, w - 1)
    #     layout = g.layout("kk")
    #     igraph.plot(g, layout=layout)
g = Graph(100)
# g.add_edge(1,3)
# g.add_edge(1,2)
# g.add_edge(2,1)
# g.add_edge(2,3)
# g.add_edge(2,5)
# g.add_edge(3,2)
# g.add_edge(3,4)
# g.add_edge(3,5)
# g.add_edge(4,3)
# g.add_edge(4,5)
# g.add_edge(5,4)
# g.add_edge(5,3)

#g.is_empty()
#g.is_complete()
# g.draw()

g.random_graph(0.3)

g.greedy_algo("l")
print("colour count", g.colour_count())
g.greedy_algo("h")
print("colour count", g.colour_count())
g.greedy_algo2()
print("colour count", g.colour_count())
