# -*- coding: utf-8 -*-
"""
Created on Sun May 17 11:41:55 2020

@author: aless
"""

import networkx as nx
import random as r

import numpy as np
#n, p = 1, .33  # n = coins flipped, p = prob of success
#s = np.random.binomial(n, p, 100)

import matplotlib.pyplot as plt


t = 50 #duration of the simulation

def build_ba_model(n,m):
    # a function that builds a B/A model 
    G = nx.generators.random_graphs.barabasi_albert_graph(n, m, seed=None)
    return G

def add_attributes(G):
    # a function that adds 'state' and 'infected_connections' attribute to each node 
    for node in G:
        G.nodes[node]['state'] = [0] #0 is susceptibale, 1 is infected, 2 is recovered -> initiliases a grid of susceptable nodes
        G.nodes[node]['infected_connections'] = [0]
        #add visited attribute that gets wiped after every time step so to speed up the function
    #print(nx.get_node_attributes(G,'state'))
    return(G)

def add_weights(G):
    # a function that adds weights to the edges of a graph
    for edge in G.edges:
        G[edge[0]][edge[1]]['weight'] = r.uniform(0, 1)
        #print( G.get_edge_data(edge[0], edge[1]))
    return

def infect(G, time, root, num, visited):
    # a recursive funtion that recuesively visits all the nodes and updates their states based on the states of their neighbours 
        state(G, num, root, time)
        for connection in G.edges(root):
            if connection not in visited:
                visited = add_edge(visited, connection)#adds edge to a list of visited edges
                connection = connection[-1] #gets the connected node
                infect(G, time, connection, G.nodes[root]['state'][time], visited)
            else:
                return

def state(G, connected_state, node, time): 
    # a function that determines the next state of the given node 
    connected = count(G, connected_state, node, time)
    print(connected)
    lst = G.nodes[node]['state'] # list of states of the specific node
    if lst[time] == 0: # if the node is susceptible 
        if len(lst)<(time+2):
            if connected_state == 1:
                x = np.random.binomial(1, 0.1) #Add probability of infection from one person here(NEED TO INCLUDE WEIGHTS)
                lst.append(x)
            else:
                lst.append(0)
        else: 
            if connected_state == 1: 
                x = np.random.binomial(1, connected*0.1) #Accounts for more then one infected neighbour (the probability for this is definetly wrong)
                lst[time+1] = x 
    elif lst[time] == 2: #if node is recovered 
        if len(lst)<(time+2):
            lst.append(2)
    elif lst[time] == 1: # if node is infected 
        if len(lst)<(time+2):
            if recover(lst): 
                lst.append(2)
            else:
                lst.append(1)
    return 

def spread(G, n): 
    # function to spread a disease over a given number of time steps 
    time = 0
    root = r.randint(0, n-1)
    G.nodes[root]['state'][time] = 1
    while time < t:
        visited =[]
        state(G, G.nodes[root]['state'][time], root, time)#updates root
        infect(G, time, root, G.nodes[root]['state'][time], visited)
        time += 1
    print(nx.get_node_attributes(G,'state'))

def add_edge(lst, edge): 
    # function that adds all the visited edges to a list
    lst.append(edge)
    new_edge = [edge[1], edge[0]]
    lst.append(new_edge)
    return lst

def percolate(G):
    # the function will remove edges from the network ..... how to do it at some time t??
    remove = [] #edges to be removed
    centralities = nx.edge_betweenness_centrality(G)
    for edge in G.edges():
        if centralities[edge] > 0.006:
            remove.append(edge)
    G.remove_edges_from(remove) # The nodes from remove are removed from the graph:

def recover(lst): 
    # function that determines whether or not an infected node recovers
    summ = 0 
    for i in lst: 
        summ += i 
    if summ >= 14: 
        return True 
    else: 
        return False

def count(G, connected_state, node, time): #check this please 
    # a function that counts the number of infected nodes connected to the given node 
    if len(G.nodes[node]['infected_connections'])<(time+2):
        G.nodes[node]['infected_connections'].append(connected_state)
    else:
        G.nodes[node]['infected_connections'][time+1] += connected_state
    return G.nodes[node]['infected_connections'][time+1]


n = 50   #S0 -> number of nodes at time t = 0.
m = 3
G = build_ba_model(n,m) #n is the number of people, m is the number of connections of each node
add_attributes(G)
add_weights(G)
spread(G,n)
#percolate(G)
#show_edges(G)
#infect(G, n)

#show the graph in python
nx.draw(G)
plt.show()

DATA = nx.get_node_attributes(G,'state')
#for every node, list of states at each time steps. length of each list = length of simulation

#running visualizer.py & using the following function:
#showSIRS(G,'simulate',0.01,0.3,0.1, t , DATA )

#find GC
#giant = max(nx.connected_component_subgraphs(G), key=len)
