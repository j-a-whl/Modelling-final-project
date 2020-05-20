import networkx as nx,
import random,
from random import choice, sample




def show_edges(G):
    lst = []
    #for node in G:
        #print(node)
    print(nx.get_node_attributes(G,'state'))
        #for connection in G.edges(node):
           # add_edge(lst, connection)
           # print(connection[-1])
       # print(lst)
        #break


# initialise B/A model
def build_ba_model(n,m):
    G = nx.generators.random_graphs.barabasi_albert_graph(n, m, seed=None)
    return G


def add_attributes(G):
    for node in G:
        G.nodes[node]['state'] = [0] #0 is susceptibale, 1 is infected, 2 is recovered -> initiliases a grid of susceptable nodes
        G.nodes[node]['infected_connections'] = [0]
    #print(nx.get_node_attributes(G,'state'))
    return(G)

def add_weights(G):
    for edge in G.edges:
        G[edge[0]][edge[1]]['weight'] = random.uniform(0, 1)
        #print( G.get_edge_data(edge[0], edge[1]))

    return



def infect(G, time, root, num, visited):
        #print(nx.get_node_attributes(G,'state'))
        state(G, num, root, time)
        for connection in G.edges(root):
            if connection not in visited:
                visited = add_edge(visited, connection)#adds edge to a list of visited edges
                connection = connection[-1] #gets the connected node
                if G.nodes[root]['state'][time] != 2: # if the node is not recovered, continue spread
                    infect(G, time, connection, G.nodes[root]['state'][time], visited)
            else:
                return

#so add another parameter to infection which is a list of all the edges that have been visited. Only edges that are not in the list are itrated over.
#The base case will be if all the edges of a node are already in the list, then return.


def state(G, connected_state, node, time): # takes the infected state of a neighbour and applies probabilites to its own states
    # needs to account for the edge weight, the number of infected individuals in contact, ...?"
    infected_connections = count(G, connected_state, node, time)  # finds the number of infected individuals in contact with the node
    if G.nodes[node]['state'][time] == 0: # checks if the node is susceptable to infection
        if len(G.nodes[node]['state'])<(time+2):
            #add infection probablities here
            G.nodes[node]['state'].append(connected_state)

        elif G.nodes[node]['state'][time+1] ==1:
            #add infection probablities here
            dice = sample(range(1, 10), 2)
            if dice[0] > 9 or dice[1]>9: # very bad but roughly 0.2 probability
                 G.nodes[node]['state'][time+1] = 1
                 # add beta probaility here and incorporate number of infected connections
            else:
                G.nodes[node]['state'][time+1] = 0

    elif G.nodes[node]['state'][time] == 1:
            if len(G.nodes[node]['state'])<(time+2): # ensures the list is of the appropriate size.
                if 14_day_infected(G.nodes[node]['state']):
                    # add recovery probability here
                    G.nodes[node]['state'].append(2)
                else:
                    G.nodes[node]['state'].append(1) # continues being infected

    return

def count(G, connected_state, node, time):
    if len(G.nodes[node]['infected_connections'])<(time+2):
        G.nodes[node]['infected_connections'].append(connected_state)
    else:
        G.nodes[node]['infected_connections'][time] += connected_state

    return G.nodes[node]['infected_connections'][time]


def 14_day_infected(lst):
    number = 0
    fourteen = 14
    for i in range(len(lit))[::-1]:
        number += lst[i]
        fourteen -= 1
        if fourteen == 0:
            break
    if number == 14:
        return True
    else:
        return False






def spread(G, n):
    time = 0
    root = random.randint(0, n-1)
    G.nodes[root]['state'][time] = 1
    while time < 10:
        visited =[]
        visited =[]state(G, G.nodes[root]['state'][time], root, time) #updates root
        infect(G, time, root, G.nodes[root]['state'][time], visited)
        time += 1
        print(nx.get_node_attributes(G,'state'))






def add_edge(lst, edge):
    lst.append(edge)
    new_edge = [edge[1], edge[0]]
    lst.append(new_edge)
    return lst



n = 20   #S0 -> number of nodes at time t = 0.
m= 3
G = build_ba_model(n,m) #n is the number of people, m is the number of connections of each node
add_attributes(G)
add_weights(G)
#show_edges(G)
spread(G, n)
#infect(G, n)
