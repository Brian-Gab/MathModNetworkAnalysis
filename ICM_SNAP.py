import snap
import random
import matplotlib.pyplot as plt

# Load SNAP graph
print("Loading graph...")
G = snap.LoadEdgeList(snap.PNGraph, "Networks/Synthetic_Data.txt", 1, 0)
print(f"Graph loaded with {G.GetNodes()} nodes and {G.GetEdges()} edges.")

# Set fixed probability
fixed_probability = 0.005
node_probabilities = {NI.GetId(): fixed_probability for NI in G.Nodes()}

# Independent Cascade Model
def ICM(G, seed_nodes, node_probabilities, max_days=14):
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
def getDailyRetweets(G, seed_nodes, fixed_probability, max_days=14, iterations=1000):
    
    node_probabilities = {node: fixed_probability for node in G.nodes()}
    daily_sums = [0] * max_days

    for j in range(iterations):
        _, daily_retweeters, _ = ICM(G, seed_nodes, node_probabilities, max_days=max_days)
        for day in range(max_days):
            daily_sums[day] += daily_retweeters[day]

    average_retweets = [round(total / iterations, 2) for total in daily_sums]

    print("===============================================================")
    print("On Probability:", fixed_probability)
    print(f"Average Retweets: {average_retweets}")
    print("===============================================================")

    return average_retweets

# plt.figure(figsize=(10, 6))
# plt.plot(range(14), daily_viewers, marker='o', linestyle='-', color='blue', label="Viewers (Seen Tweet)")
# plt.plot(range(14), averageRetweets, marker='s', linestyle='--', color='red', label="Retweeters (New RTs)")

# plt.xlabel("Days")
# plt.ylabel("Number of People")
# plt.title("Spread of Tweet Viewers and Retweeters Over 14 Days")
# plt.legend()
# plt.grid()
# plt.show()

# Print results
# print("=================================================================")
# print("- On Probability:", fixed_probability, " -")
# print(f"Daily Viewers (Total Seen): {daily_viewers}")
# print(f"Total Views on Day 14:", sum(daily_viewers))
# print()
# print(f"Daily Retweeters (New Retweets): {daily_retweeters}")
# print(f"Total Retweets on Day 14:", sum(daily_retweeters))
# print("=================================================================")
