import snap
import random
import networkx as nx
import matplotlib.pyplot as plt

# Load SNAP graph
print("Loading graph...")
G = snap.LoadEdgeList(snap.PNGraph, "Networks/test.csv", 1, 0)
print(f"Graph loaded with {G.GetNodes()} nodes and {G.GetEdges()} edges.")

# Set fixed probability
fixed_probability = 0.003
node_probabilities = {NI.GetId(): fixed_probability for NI in G.Nodes()}

# Independent Cascade Model
def independent_cascade_full(G, seed_nodes, node_probabilities, max_days=14):
    activated_nodes = set(seed_nodes)
    new_active = set(seed_nodes)
    daily_viewers = [len(new_active)]
    daily_retweeters = [len(new_active)]

    for day in range(1, max_days):
        next_active = set()
        viewers_today = set(new_active)
        
        for node in new_active:
            NI = G.GetNI(node)
            for neighbor in NI.GetOutEdges():
                if neighbor not in activated_nodes:
                    viewers_today.add(neighbor)
                    if random.random() < node_probabilities[neighbor]:
                        next_active.add(neighbor)

        activated_nodes.update(next_active)
        new_active = next_active

        daily_viewers.append(len(viewers_today))
        daily_retweeters.append(len(next_active))

    return daily_viewers, daily_retweeters, activated_nodes

# Run the cascade
seed_nodes = [0]
daily_viewers, daily_retweeters, activated_nodes = independent_cascade_full(G, seed_nodes, node_probabilities, max_days=14)

# Print results
print("=================================================================")
print("- On Probability:", fixed_probability, " -")
print(f"Daily Viewers (Total Seen): {daily_viewers}")
print(f"Total Views on Day 14:", sum(daily_viewers))
print()
print(f"Daily Retweeters (New Retweets): {daily_retweeters}")
print(f"Total Retweets on Day 14:", sum(daily_retweeters))
print("=================================================================")
