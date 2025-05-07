import networkx as nx
import random
import matplotlib.pyplot as plt

# Independent Cascade Model using NetworkX
def ICM(G, seed_nodes, node_probabilities, max_days=14):
    activated_nodes = set(seed_nodes)
    new_active = set(seed_nodes)
    daily_viewers = [len(new_active)]
    daily_retweeters = [len(new_active)]

    for day in range(1, max_days):
        next_active = set()
        viewers_today = set(new_active)

        for node in new_active:
            for neighbor in G.successors(node):  # Out-edges in directed graph
                if neighbor not in activated_nodes:
                    viewers_today.add(neighbor)
                    if random.random() < node_probabilities.get(neighbor, 0):
                        next_active.add(neighbor)

        activated_nodes.update(next_active)
        new_active = next_active

        daily_viewers.append(len(viewers_today))
        daily_retweeters.append(len(next_active))

    return daily_viewers, daily_retweeters, activated_nodes

# Run the cascade
def runCascae(filepath, seed_nodes, fixed_probability, max_days=14):
    retweets = []
    viewers = []
    G = nx.DiGraph()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                followed, follower = parts[1], parts[0]
                G.add_edge(follower, followed)  # B → A (follower → followed)
    print(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    node_probabilities = {node: fixed_probability for node in G.nodes()}

    for j in range(1, 1000):
        daily_viewers, daily_retweeters, activated_nodes = ICM(G, seed_nodes, node_probabilities, max_days=max_days)
        retweets.append(sum(daily_retweeters))
        viewers.append(sum(daily_viewers))
    
    average_retweets = sum(retweets) / len(retweets)
    average_viewers = sum(viewers) / len(viewers)

    print("===============================================================")
    print("For Anji On Probability:", fixed_probability)
    print("Average Retweets:", average_retweets)
    print("Average Viewers:", average_viewers)
    print("===============================================================")
        

print("Loading Anji's graph...")
runCascae("Networks/Anji_real.txt", ["anjisalvacion"], 0.004246426309, max_days=14)
print("")
print("Loading Maxie's Graph...")
runCascae("Networks/Maxie_real.txt", ["maxieandreison"], 0.004246426309, max_days=14)

# # Print results
# print("=================================================================")
# print("- On Probability:", fixed_probability, " -")
# print(f"Daily Viewers (Total Seen): {daily_viewers}")
# print(f"Total Views on Day 14:", sum(daily_viewers))
# print()
# print(f"Daily Retweeters (New Retweets): {daily_retweeters}")
# print(f"Total Retweets on Day 14:", sum(daily_retweeters))
# print("=================================================================")

# plt.figure(figsize=(10, 6))
# #plt.plot(range(14), daily_viewers, marker='o', linestyle='-', color='blue', label="Viewers (Seen Tweet)")
# plt.plot(range(14), daily_retweeters, marker='s', linestyle='--', color='red', label="Retweeters (New RTs)")

# plt.xlabel("Days")
# plt.ylabel("Number of People")
# plt.title("Spread of Tweet Viewers and Retweeters Over 14 Days")
# plt.legend()
# plt.grid()
# plt.show()

# Visualize the activated subgraph
# def visualize_activated_subgraph(G_snap, activated_nodes):

#     pos = nx.spring_layout(G, seed=42)  # layout for consistent positioning

#     plt.figure(figsize=(10, 7))
#     nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, arrowsize=15)
#     plt.title("Activated Subgraph after Independent Cascade")
#     plt.show()

# # Call visualization function
# visualize_activated_subgraph(G, activated_nodes)
