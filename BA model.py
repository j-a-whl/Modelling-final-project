import networkx as nx, random
from random import choice, sample



def show_edges(G):
    for node in G:
        print(node)

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
        G[edge[0]][edge[1]]['weight'] = random.uniform(0, 1)
        #print( G.get_edge_data(edge[0], edge[1]))
        
    return


                
def infect(G, time, root, num):
        state(G, num, root, time)
        for connection in G.edges(root):
            connection = connection[-1] #gets the connected node
            if G.nodes[root]['state'][time] != 2: # if the node is not recovered, continue spread 
                infect(G, time, connection, G.nodes[root]['state'][time])
                return
        
#so add another parameter to infection which is a list of all the edges that have been visited. Only edges that are not in the list are itrated over. 
#The base case will be if all the edges of a node are already in the list, then return. 
           
    
def state(G, connected_state, node, time): #takes the infected state of a neighbour and applies probabilites to its own states
    
    #needs to account for the edge weight, the number of infected individuals in contact, ...?" 
    
    if G.nodes[node]['state'][time] == 0: #checks if the node is susceptable to infection 
        if connected_state == 1 and len(G.nodes[node]['state'])<(time+2): 
            #add infection probablities here
            G.nodes[node]['state'].append(connected_state)
        
    
    elif G.nodes[node]['state'][time] == 1: #
         #add recovery probabilities here 
         pass
    
    return
    
    
    

def spread(G, n): 
    root = random.randint(0, n)
    time = 0
    while time < 10:
        state(G, G.nodes[root]['state'][time], root, time) #updates root 
        infect(G, time, root, G.nodes[root]['state'][time])
        time += 1
        print(nx.get_node_attributes(G,'state'))
        
    
    

            
        
    
            


n = 20   #S0 -> number of nodes at time t = 0. 
m= 4
G = build_ba_model(n,m) #n is the number of people, m is the number of connections of each node 
add_attributes(G)
add_weights(G)
show_edges(G)
spread(G, n)
#infect(G, n)
