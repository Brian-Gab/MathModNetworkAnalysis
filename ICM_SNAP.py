import snap
import random
import networkx as nx
import matplotlib.pyplot as plt

# Load SNAP graph
print("Loading graph...")
G = snap.LoadEdgeList(snap.PNGraph, "Networks/Anji_test.txt", 1, 0)
print(f"Graph loaded with {G.GetNodes()} nodes and {G.GetEdges()} edges.")

# Set fixed probability
fixed_probability = 0.005
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

day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, day14 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
iterations = 101

for j in range(1, iterations):
    daily_viewers, daily_retweeters, activated_nodes = independent_cascade_full(G, seed_nodes, node_probabilities, max_days=14)
    day1 += daily_retweeters[0]
    day2 += daily_retweeters[1]
    day3 += daily_retweeters[2]
    day4 += daily_retweeters[3]
    day5 += daily_retweeters[4]
    day6 += daily_retweeters[5]
    day7 += daily_retweeters[6]
    day8 += daily_retweeters[7]
    day9 += daily_retweeters[8]
    day10 += daily_retweeters[9]
    day11 += daily_retweeters[10]
    day12 += daily_retweeters[11]
    day13 += daily_retweeters[12]
    day14 += daily_retweeters[13]

averageRetweets = [round(day1/iterations, 2), round(day2/iterations, 2), round(day3/iterations, 2), round(day4/iterations, 2), round(day5/iterations, 2), round(day6/iterations, 2), round(day7/iterations, 2), round(day8/iterations, 2), round(day9/iterations, 2), round(day10/iterations, 2), round(day11/iterations, 2), round(day12/iterations, 2), round(day13/iterations, 2), round(day14/iterations, 2)] 
print(f"Average Retweets: {averageRetweets}")

plt.figure(figsize=(10, 6))
#plt.plot(range(14), daily_viewers, marker='o', linestyle='-', color='blue', label="Viewers (Seen Tweet)")
plt.plot(range(14), averageRetweets, marker='s', linestyle='--', color='red', label="Retweeters (New RTs)")

plt.xlabel("Days")
plt.ylabel("Number of People")
plt.title("Spread of Tweet Viewers and Retweeters Over 14 Days")
plt.legend()
plt.grid()
plt.show()

# Print results
# print("=================================================================")
# print("- On Probability:", fixed_probability, " -")
# print(f"Daily Viewers (Total Seen): {daily_viewers}")
# print(f"Total Views on Day 14:", sum(daily_viewers))
# print()
# print(f"Daily Retweeters (New Retweets): {daily_retweeters}")
# print(f"Total Retweets on Day 14:", sum(daily_retweeters))
# print("=================================================================")
