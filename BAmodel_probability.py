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



def show_edges(G):
    lst = []
    #for node in G:
    #   print(node)
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
    #print(nx.get_node_attributes(G,'state'))
    return(G)

def add_weights(G):
    for edge in G.edges:
        G[edge[0]][edge[1]]['weight'] = r.uniform(0, 1)
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
           
    
def state(G, connected_state, node, time): #takes the infected state of a neighbour and applies probabilites to its own states
      
    neighbors = [n for n in G[node]] #list of neighbors connected to a given node
    x = G.nodes[node]['state'] #list of states of the specific node
   
    for neighbor in neighbors:
        if G.nodes[neighbor]['state'][time] == connected_state: #checks if any neighboring node is in state 1 at some time
            
            if x[time] == 0: #checks if the node is susceptable to infection at some time 
                if len(x)<(time+2): #check for appropriate list size
            
                    x[time] = np.random.binomial(1, 0.1)            
                # updates its own state, of the node x, will either stay 0 or become 1 
                #(with probability 0.01 of becoming 1, infected),at a specifc time
             
                    x.append(x[time]) 
                #appends the new state at spec time 
                #(which wither shifted to 1 or stayed 0 based on some prob)
                #to the list of states x
    
            elif x[time] == 1: 
                if len(x)<(time+2):#ensures the list is of the appropriate size. 
                    x.append(1) #continues being infected
         

            return
        

def spread(G, n): 
    time = 0
    root = r.randint(0, n-1)
    G.nodes[root]['state'][time] = 1
    while time < t:
        visited =[]
        visited =[state(G, G.nodes[root]['state'][time], root, time)] #updates root 
        infect(G, time, root, G.nodes[root]['state'][time], visited)
        time += 1
        print(nx.get_node_attributes(G,'state'))
        
    
            
def add_edge(lst, edge): 
    lst.append(edge)
    new_edge = [edge[1], edge[0]]
    lst.append(new_edge)
    return lst

def percolate(G):
#the function will remove edges from the network ..... how to do it at some time t??
    remove = [] #edges to be removed
    centralities = nx.edge_betweenness_centrality(G)
    
    for edge in G.edges():
        if centralities[edge] > 0.006:
            remove.append(edge)

#The nodes from remove are removed from the graph:    
    G.remove_edges_from(remove)
            


n = 50   #S0 -> number of nodes at time t = 0. 
m= 3
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
showSIRS(G,'simulate',0.01,0.3,0.1, t , DATA )

#find GC
#giant = max(nx.connected_component_subgraphs(G), key=len)






