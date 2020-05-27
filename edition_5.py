#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 13:34:36 2020

@author: xox
"""

import networkx as nx
import random as r
import numpy as np
import matplotlib.pyplot as plt

#graph attribute and altering code 

def build_ba_model(n,m):
    # a function that builds a B/A model 
    G = nx.generators.random_graphs.barabasi_albert_graph(n, m, seed=None)
    
    return G

def add_attributes(G):
    # a function that adds 'state' and 'infected_connections' attribute to each node 
    for node in G:
        G.nodes[node]['state'] = [0] #0 is susceptibale, 1 is infected, 2 is recovered -> initiliases a grid of susceptable nodes
        G.nodes[node]['infected_connections'] = [0]
    return(G)
    
def add_weights(G):
    # a function that adds weights to the edges of a graph
    for edge in G.edges:
        G[edge[0]][edge[1]]['weight'] = r.uniform(0, 1)
    return

def add_edge(lst, edge): 
    # function that adds all the visited edges to a list
    lst.append(edge)
    new_edge = [edge[1], edge[0]]
    lst.append(new_edge)
    return lst

def count(G, connected_state, node, time): #check this please 
    # a function that counts the number of infected nodes connected to the given node 
    if len(G.nodes[node]['infected_connections'])<(time+2):
        G.nodes[node]['infected_connections'].append(connected_state)
    else:
        G.nodes[node]['infected_connections'][time+1] += connected_state
    return G.nodes[node]['infected_connections'][time+1]

def setup(n, m): 
    G = build_ba_model(n,m) #n is the number of people, m is the number of connections of each node
    random_choose(G, 0.2) # percentages of edges that are going to be removed
    add_attributes(G)
    add_weights(G)
    return G

#code for spreading of the infection 

def infect(G, time, root, num, visited, weight):
    # a recursive funtion that recuesively visits all the nodes and updates their states based on the states of their neighbours 
        state(G, num, root, time, weight)
        for connection in G.edges(root):
            if connection not in visited:
                weight = G[connection[0]][connection[1]]['weight']
                #print(weight)
                visited = add_edge(visited, connection)#adds edge to a list of visited edges
                connection = connection[-1] #gets the connected node
                infect(G, time, connection, G.nodes[root]['state'][time], visited, weight)
            else:
                return    

def spread(G, n): 
    # function to spread a disease over a given number of time steps 
    time = 0
    root = r.randint(0, n-1)
    G.nodes[root]['state'][time] = 1
    weight = 1 # initial weight for root infected node, not important
    while time < t:
        if time == 0: 
            perc_giant(G, root) # based on edge between centrality 
            rm_edge_weight(G, 0.5) # social distancing 
        visited =[]
        state(G, G.nodes[root]['state'][time], root, time, weight) # updates root
        infect(G, time, root, G.nodes[root]['state'][time], visited, weight)
        time += 1
    
    
# probabilities code 

def state(G, connected_state, node, time, weight): 
    # a function that determines the next state of the given node 
    connected = count(G, connected_state, node, time)
    lst = G.nodes[node]['state'] # list of states of the specific node
    if lst[time] == 0: # if the node is susceptible 
        if len(lst)<(time+2):
            if connected_state == 1:
                x = np.random.binomial(1, 0.2*weight) # Add probability of infection from one person here(NEED TO INCLUDE WEIGHTS)
                lst.append(x)
            else:
                lst.append(0)
        else:
            if lst[time+1] == 0 and connected_state == 1: # if the node has been in contact with infected indivduals 
                x = np.random.binomial(1, 0.2*weight) # Add probability of infection from one person here(NEED TO INCLUDE WEIGHTS)
                lst[time+1] = x      
    elif lst[time] == 2: # if node is recovered 
        if len(lst)<(time+2):
            lst.append(2)
            
    elif lst[time] == 1: # if node is infected 
        if len(lst)<(time+2):
            if recover(lst, node, G):
                lst.append(2)
            else:
                lst.append(1)
    return 
    
def recover(lst, node, G): 
    # function that determines whether or not an infected node recovers
    summ = 0
    num = r.randint(14, 35) # randomly chooses the length of infectious period of individual
    for i in lst: 
        summ += i 
    if summ >= 14: 
        weight_to_zero(G, node) # after fourteen days -> go into isolation
    if summ >= num: 
        return True 
    else: 
        return False

# Data code 

def data(G):
    DATA = nx.get_node_attributes(G,'state') #dictionary -> node : [list of states of that node for all times]
    tot_S = [] #shoudl look like this tot_S = [100, 99....0]
    tot_I = [] # should look like this tot_I = [1, 2, ......peak.....decreasing]
    tot_R = [] #shoudl look like this = [0,0,0,0,0,........1,2,3....increasing]
    data = [tot_S, tot_I, tot_R]
    
    for time in range(t):
        
        my_list = [elem[time] for elem in DATA.values()]      #list of states at a given time step 
        
        s = my_list.count(0) #counts how many values are in state 0 - how many nodes are infected at time
        tot_S.append(s)
        
        i = my_list.count(1)
        tot_I.append(i)
        
        r = my_list.count(2)
        tot_R.append(r)
        
    print(max(tot_I))
    print(tot_I.index(max(tot_I)))
    return data    

# perculation code 

def weight_to_zero(G, node):
    # takes in a node and makes all its edge weights = 0: 
    for edge in G.edges(node): 
        G[edge[0]][edge[1]]['weight'] == 0 
    

def rm_edge_weight(G, threshold): # negates edges below a certain threshold. (discard if their weight is below the threshold)
    for node in G:
        for edge in G.edges(node):
            if G[edge[0]][edge[1]]['weight'] <= threshold:
                G[edge[0]][edge[1]]['weight'] = 0
        
def percolate(G):
    # the function will remove edges from the network ..... how to do it at some time t??
    remove = [] #edges to be removed
    centralities = nx.edge_betweenness_centrality(G)
    for edge in G.edges(): 
        if centralities[edge] > 0.05:
            remove.append(edge)
    for edge in remove: 
        G[edge[0]][edge[1]]['weight'] = 0 
    return 

def random_choose(G, cut_prob):
    # randomly negates certain edges of a graph 
    chosen = []
    for node in G: 
        for edge in G.edges(node): 
            x = np.random.binomial(1, cut_prob) #percentage of edges that will be cut in the beginning 
            if x == 1:
                chosen.append(edge)
                #G[edge[0]][edge[1]]['weight'] = 0
    G.remove_edges_from(chosen)
    print(chosen)
    return
 
def perc_giant(G, root): 
    #isolates the giant coimponent of a graph and return a list of nodes in the giant component
    lst_of_nodes = []
    giant = max(nx.connected_component_subgraphs(G), key=len)
    edge_list = nx.edge_boundary(G, giant.nodes(), nbunch2=None)
    print(nx.info(giant))
    for edge in edge_list: 
        G[edge[0]][edge[1]]['weight'] = 0.01
    if root in giant.nodes():
        percolate(giant)
    for node in giant: 
        lst_of_nodes.append(node)
    return lst_of_nodes



if __name__ == "__main__":
    n = 100  #S0 -> number of nodes at time t = 0.
    m = 3
    G = setup(n, m)
    spread(G,n)
    nx.draw(G)
    plt.show()
    plt.plot(data(G)[0]) #plotting time evolution of nuber of susceptible fellas
    plt.plot(data(G)[1]) #plotting time evolution of number of infected fellas
    plt.plot(data(G)[2]) #plotting time evoluition of number of recovered fellas
