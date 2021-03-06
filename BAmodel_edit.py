# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:47:19 2020

@author: aless
"""

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

t = 100 #duration of the simulation

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
            
def edge_counter(G, node): 
    num = 0
    for connection in G.edges(node):
        num += 1
    return num 

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
            '''
            if connected_state == 1: 
                x = np.random.binomial(1, 0.05*(1+(connected)/edge_counter(G, node))) # beta *(1+infected connected nodes/total connected nodes)
                lst[time+1] = x 
            '''
            
    elif lst[time] == 2: # if node is recovered 
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
    weight = 1 # initial weight for root infected node, not important 
    while time < t:
        visited =[]
        state(G, G.nodes[root]['state'][time], root, time, weight) # updates root
        infect(G, time, root, G.nodes[root]['state'][time], visited, weight)
        time += 1
    #print(nx.get_node_attributes(G,'state'))

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
        if centralities[edge] > 0.006: #removes bases on threshold -> we could also remove based on number. 
            remove.append(edge)
    G.remove_edges_from(remove) # The nodes from remove are removed from the graph:

def recover(lst): 
    # function that determines whether or not an infected node recovers
    summ = 0
    num = r.randint(20, 50) # randomly chooses the length of infectious period of individual
    for i in lst: 
        summ += i 
    if summ >= num: 
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

def rm_edge_weight(G, n): # removes every edges top n weighted nodes
    for node in G:
        top = []
        for edge in G.edges(node):
            if len(top)<(n):
                top.append(edge)
                top.sort()
            elif G[edge[0]][edge[1]]['weight'] > top[0]: 
                top = top[1:]
                top.append(edge)
                top.sort()
        G.remove_edges_from(top) 
                
    
            


def data(G):
#to return a list, data, cointaing the three lists tot_S, tot_I and tot_R.
# each of theses three lists, of length t, contains the total number
# of nodes in state S,I,R respectively, at each time step.
#so data[1][45] would give us the total number of nodes that were susceptible at t=45,
# and data[2][45] woudl give us the total number of infected nodes at t=45 .... ect
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


    return data           
            
            
            
            
            
n = 200   #S0 -> number of nodes at time t = 0.
m = 3
G = build_ba_model(n,m) #n is the number of people, m is the number of connections of each node
add_attributes(G)
add_weights(G)
percolate(G) #doesn't seem to flatten the I curve that much lol - only by ~30 peoplea at the peak..
spread(G,n)

#show_edges(G)
#infect(G, n)

#show the graph in python
nx.draw(G)
plt.show()

plt.plot(data(G)[0]) #plotting time evolution of nuber of susceptible fellas
plt.plot(data(G)[1]) #plotting time evolution of number of infected fellas
plt.plot(data(G)[2]) #plotting time evoluition of number of recovered fellas

#DATA = nx.get_node_attributes(G,'state')
#for every node, list of states at each time steps. length of each list = length of simulation

#running visualizer.py & using the following function:
#showSIRS(G,'simulate',0.01,0.3,0.01, t , data(G) )

#find GC
#giant = max(nx.connected_component_subgraphs(G), key=len)