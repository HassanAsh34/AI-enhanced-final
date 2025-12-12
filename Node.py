import networkx as nx
import random
import matplotlib.pyplot as plt

class Node:
    _counter = 0

    def __init__(self,flag=False):
        if flag:
            Node._counter = 0
        else:
            Node._counter +=1
            self.Id = Node._counter
            self.edges = []
            # self.color = ""
            self.color = -1
    def addEdge(self,node):
        if type(node) is list:
            # for n in node:
            #     if n not in self.edges:
            #         self.edges.append(n)
            self.edges.extend(node)
            self.edges = list(set(self.edges))
        else:
            if node not in self.edges:
                self.edges.append(node)
        # shape = "Circle"
    def isSafe(self,color):
        for node in self.edges:
            if(color.lower() == node.color.lower()):
                return False
        return True

    def isSafeCanonical(self,color):
        for node in self.edges:
            if(color == node.color):
                return False
        return True


def printGraph(g,optimal,colors):
    pos = nx.spring_layout(g)
    edge_labels = {(u, v): f"{u}-{v}" for u, v in g.edges}
    # if
    if optimal != None:
        optimal = random.choice(optimal)
        color = []
        for i in optimal:
            color.append(colors[i])
        nx.draw(g,node_color= color, pos=pos, with_labels=True, node_size=800, font_weight="bold")


    else:
        nx.draw(g,pos=pos, with_labels=True, node_size=800, font_weight="bold")

    if edge_labels.items():
        print(edge_labels)
        nx.draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels)
    plt.show()

def printGraphGUI(g,ax,optimal,colors,canvasA,canvasB = None):
    ax.clear()
    pos = nx.spring_layout(g)
    edge_labels = {(u, v): f"{u}-{v}" for u, v in g.edges}
    chromatic_number = None
    # if
    if optimal is not None and len(optimal) > 0:
        optimal = random.choice(optimal)
        color = []
        for i in optimal:
            color.append(colors[i])
        chromatic_number = len(set(color))
        nx.draw(g,node_color= color, pos=pos, with_labels=True, node_size=800, font_weight="bold",ax=ax)


    else:
        nx.draw(g,pos=pos, with_labels=True, node_size=800, font_weight="bold",ax=ax)

    if edge_labels.items():
        print(edge_labels)
        nx.draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels,ax=ax)

    if chromatic_number is not None:
        ax.text(0.5, 1.05, f"Chromatic Number: {chromatic_number}",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=10, fontweight='bold', color='black')

    canvasA.draw()
    if canvasB is not None:
        canvasB.draw()


def addEdgesGUI(g,nodes,edges):
    try:
        a, b = map(int, edges.split())
        if a in g.nodes and b in g.nodes:
            t = tuple(sorted((a,b)))
            if t in g.edges:
                return  "edge already exists"
            else:
                n1 = n2  = None
                for node in nodes:
                    if(node.Id == a or node.Id == b):
                        if n1 == None:
                            n1 = node
                        elif n2 == None and n1 != None:
                            n2 = node
                        else:
                            continue
                if n1 is not None and n2 is not None:
                    if isinstance(n1, Node) and isinstance(n2, Node):
                        g.add_edge(a, b)
                        n1.addEdge(n2)
                        n2.addEdge(n1)
                        return 1
                    else:
                        return "Something went wrong with IDs or node lookup."
                else:
                    return "something gone wrong with ids"
        else:
            return "Invalid node IDs."
    except ValueError:
        return "Enter two numbers separated by a space."


def addEdges(g,nodes,edges):
    try:
        a, b = map(int, edges.split())
        if a in g.nodes and b in g.nodes:
            t = tuple(sorted((a,b)))
            if t in g.edges:
                print("edge already exists")
            else:
                n1 = n2  = None
                for node in nodes:
                    if(node.Id == a or node.Id == b):
                        if n1 == None:
                            n1 = node
                        elif n2 == None and n1 != None:
                            n2 = node
                        else:
                            continue
                if n1 is not None and n2 is not None:
                    if isinstance(n1, Node) and isinstance(n2, Node):
                        g.add_edge(a, b)
                        n1.addEdge(n2)
                        n2.addEdge(n1)
                        print(f"Connected node {n1.Id} with {n2.Id}")
                    else:
                        print("Something went wrong with IDs or node lookup.")
                else:
                    print("something gone wrong with ids")
        else:
            print("Invalid node IDs.")
    except ValueError:
        print("Enter two numbers separated by a space.")

def addEdgesRandomly(g,node,nodes):
    if node.Id == node._counter:
        # print("randomly added edges")
        return
    else:
        edges = random.sample(nodes,random.randint(1,len(nodes)-1))
        # print(edges)
        for edge in edges:
            if edge.Id != node.Id:
                edge.addEdge(node)
                g.add_edge(node.Id,edge.Id)
            else:
                edges.remove(edge)
        node.addEdge(edges)
        id = node.Id+1
        return addEdgesRandomly(g,nodes[id-1],nodes)

def evaluateSolutions(solutions,CA = False):
    evaluatedSols = list()
    for sol in solutions:
        chromaticnum = len(set(sol))
        if CA == False:
            evaluatedSols.append((chromaticnum,sol))
        else:
            evaluatedSols.append(chromaticnum)
    if CA == False:
        evaluatedSols.sort(key= lambda x: x[0])
    return evaluatedSols