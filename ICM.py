import random
import networkx as nx

G = nx.Graph()
with open('Networks/Maxie_real.txt', 'r') as f:
    for line in f:
        nodes = line.strip().split()
        if len(nodes) == 2:
            G.add_edge(nodes[0], nodes[1])

def independent_cascade(G, seeds, p=0.1, max_steps = 3):
    active_nodes = set(seeds)
    newly_activated = set(seeds)
    step = 0

    while newly_activated and step < max_steps:
        next_newly_activated = set()
        for node in newly_activated:
            neighbors = set(G.neighbors(node)) - active_nodes
            for neighbor in neighbors:
                if random.random() < p:
                    next_newly_activated.add(neighbor)
                    active_nodes.add(neighbor)

        newly_activated = next_newly_activated
        step += 1

    return active_nodes

time = 1
p = 0.004
while(time <= 14):
    seeds = ['maxieandreison']
    activated_nodes = independent_cascade(G, seeds, p, max_steps=time)
    num_activated_nodes = len(activated_nodes)
    print("Activated Nodes Count on Time", time, "under probability", p, ": ", num_activated_nodes)
    time = time+1

print()