import random
import collections
import igraph
import operator
from operator import itemgetter
import itertools
import time

class Graph():
    def __init__(self, n):
        self.graph_size = n
        self.edge_list = {}      # a dictionary where keys are the vertices and the values are the set of neighbours
        self.edge_cnt = 0        # number of edges
        self.vertex_colour = {}
        self.vertex_degree = {}
        for x in range(1, n+1):
            self.edge_list[x] = set()
            self.vertex_colour[x] = 0

    def add_edge(self, a, b):
        """ Add edge between the vertices a and b to graph"""
        if a > self.order():
            print "Can not add edge because", a, "is not a vetex in the graph."
        elif b > self.order():
            print "Can not add edge because", b, "is not a vetex in the graph."
        elif a != b:
            self.edge_list[a].add(b)
            self.edge_list[b].add(a)
            self.edge_cnt = self.edge_cnt + 1

    def print_graph(self):
        """Print graph to console"""
        if self.is_empty():
            print "Graph is empty!"
        else:
            for j in range(1, self.graph_size +1):
                    print "vertex",j, "neighbours", self.edge_list[j],"colour",self.vertex_colour[j]

    def clear(self):
        """Clear sets (edges)"""
        for j in range(1, self.order()+1):
            self.edge_list[j].clear()
        self.edge_cnt=0

    def order(self):
        """Return the number of edges in the graph"""
        return len(self.edge_list)

    def size(self):
        """Return the number of edges in the graph"""
        return self.edge_cnt

    def remove_edge(self, a, b):
        """remove an edge"""
        if b in self.edge_list[a]:
            self.edge_list[a].remove(b)
            self.edge_list[b].remove(a)
            self.edge_cnt = self.edge_cnt - 1

    def is_empty(self):
        """Check if the graph is empty"""
        if self.edge_cnt!=0:
            return False
        return True

    def is_complete(self):
        """Check if the graph is complete (all vertices are connected to each other)"""
        if self.edge_cnt==self.order()*(self.order()-1)/2:
            return True
        return False


    def naive_colouring(self):
        ### random colours but can have duplicates
        for k in range(1, self.order() + 1):
            self.vertex_colour[k]=random.randint(0, self.order())

        ### vertex colour is added in order from 1 to vertex's number then values are shuffled (no duplicate colours)
        for k in range(1, self.order() + 1):
            self.vertex_colour[k] = k
        values = list( )
        random.shuffle(values)
        self.vertex_colour= dict(zip(self.vertex_colour.keys(), values))
        print (self.vertex_colour)

    def colour_count(self):
        """Count colours in the graph"""
        if self.vertex_colour[1] == 0:
            return 0
        else:
            colour_set = set(self.vertex_colour.values()) # colours are a set to remove duplicates, then it gets the len
            return (len(colour_set))

    def clear_colour(self):
        for vertex in range(1, self.order() + 1):
            self.vertex_colour[vertex]=0

    def degree_lowest(self):
        """Arrange a dict of vertices and edges starting from the lowest degree"""
        vertex_degree={}
        for v in range(1, self.order() + 1):
            vertex_degree[v] = len(self.edge_list[v])
        sorted_degree = sorted(vertex_degree.items(), key=operator.itemgetter(1))
        order_lowest = []
        for a, b in sorted_degree:
            order_lowest.append(a)
        return order_lowest

    def degree_highest(self):
        """Order the vertices by highest degree"""
        l = self.degree_lowest()
        l.reverse()
        return l

    def is_proper(self):
        for vertex in range(1, self.graph_size + 1):
            for neighbour in self.edge_list[vertex]:
                if self.vertex_colour[vertex] == self.vertex_colour[neighbour]:
                    return False
        return True


    def colour_greedy(self,order_deg):
        """Colour graphs using the greedy algorithm depending on the vertex degree"""
        for x in range(1,self.graph_size +1):
            self.vertex_colour[x]=0
        if order_deg == "l":
            v = self.degree_lowest()
        elif order_deg == "h":
            v = self.degree_highest()
        elif order_deg == "n":
            v= range(1,self.graph_size +1)
        for j in range(0, len(v)):
            nb = list(self.edge_list[v[j]])  # place the neighbours in a list
            colour = {}  # empty colour dict
            for i in range(1, self.graph_size + 1):  # loop to set all colours to be available
                colour[i] = True
            # loop checks if all the vertex neighbours have a colour, if they do, the colour is "false" (unavailable)
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

    def random_graph(self, p):
        """Generate a random graph"""
        self.clear()
        for v1 in range(1, self.graph_size + 1):
            for v2 in range(v1, self.graph_size + 1):
                if v1 != v2 and random.random() < p:
                    self.add_edge(v1,v2)

   def colour_brute(self):
        for palette_size in range(1, self.order()+1):
            for assignment in itertools.product(range(1,palette_size), repeat=self.order()):
                self.vertex_colour = dict(zip(self.edge_list.keys(), assignment))
                print assignment
                if self.is_proper():
                    return
        print "Complete graph! %d colours needed." %(self.order())

    def is_safe(self, c, nb):
        """check if colour is safe"""
        for x in nb:
            if self.vertex_colour[x] == c:
                return False
        return True

    def gcu(self, m, v):
        if (v == self.order()+1):
            return True

        for c in range(1, m + 1):
            nb = list(self.edge_list[v])
            if self.is_safe(c, nb):
                self.vertex_colour[v] = c
                if self.gcu(m, v + 1) == True:
                    return True
            g.vertex_colour[v]=0
        return False

    def colour_backtracking(self, m):
        if self.gcu(m, 1) == False:
            print"can't color with %d" % (m)
            return False
        return True

    def draw(self):
         g = igraph.Graph()
         g.add_vertices(self.order())
         for v in range(1, self.order()+1):
             for w in range(v+1, self.order()+1):
                 if w in self.edge_list[v]:
                     g.add_edge(v-1, w-1)
         layout = g.layout("kk")
         igraph.plot(g, layout = layout)
