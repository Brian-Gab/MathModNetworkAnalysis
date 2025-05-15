import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error
import numpy as np

fixedProbability = 0.005
Anji_filepath = "Networks/Anji_real.txt"
Maxie_filepath = "Networks/Maxie_real.txt"
Maxie_seed = ["maxieandreison"]

# Import Graph from file
def importGraph(filepath):
    print(f"Loading graph from {filepath}...")
    G = nx.DiGraph()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                followed, follower = parts[1], parts[0]
                G.add_edge(follower, followed)  # B → A (follower → followed)
    print(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    return G

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
def getAverageRetweets(filepath, seed_nodes, fixed_probability=fixedProbability, max_days=14, iterations=1000):
    retweets = []
    viewers = []

    G = importGraph(filepath)
    node_probabilities = {node: fixed_probability for node in G.nodes()}

    for j in range(1, iterations+1):
        daily_viewers, daily_retweeters, activated_nodes = ICM(G, seed_nodes, node_probabilities, max_days=max_days)
        retweets.append(sum(daily_retweeters))
        viewers.append(sum(daily_viewers))
    
    average_retweets = sum(retweets) / len(retweets)
    average_viewers = sum(viewers) / len(viewers)

    print("===============================================================")
    print("On Probability:", fixed_probability)
    print("Average Retweets:", average_retweets)
    print("Average Viewers:", average_viewers)
    print("===============================================================")
    return average_retweets, average_viewers, activated_nodes
        
def getDailyRetweets(filepath, seed_nodes, fixed_probability=fixedProbability, max_days=14, iterations=1000):
    G = importGraph(filepath)
    node_probabilities = {node: fixed_probability for node in G.nodes()}

    daily_sums = [0] * max_days
    daily_views = [0] * max_days

    for j in range(iterations):
        daily_viewers, daily_retweeters, _ = ICM(G, seed_nodes, node_probabilities, max_days=max_days)
        for day in range(max_days):
            daily_sums[day] += daily_retweeters[day]
            daily_views[day] += daily_viewers[day]

    average_retweets = [round(total / iterations, 2) for total in daily_sums]
    average_viewers = [round(total / iterations, 2) for total in daily_views]

    # print("===============================================================")
    # print("On Probability:", fixed_probability)
    # print(f"Average Retweets: {average_retweets}")
    # print(f"Average Viewers: {avergae_viewers}"")
    # print("===============================================================")

    return average_retweets, average_viewers


def plotGraph(daily_viewers, averageRetweets):
    plt.figure(figsize=(10, 6))
    plt.plot(range(14), daily_viewers, marker='o', linestyle='-', color='blue', label="Viewers (Seen Tweet)")

    plt.xlabel("Days")
    plt.ylabel("Number of People")
    plt.title("Spread of Tweet Viewers and Retweeters Over 14 Days")
    plt.legend()
    plt.grid()
    plt.show()

def getTopActivatedNodes(filepath, seed_nodes, fixed_probability=fixedProbability, max_days=14, iterations=1000):
    G = importGraph(filepath)
    node_probabilities = {node: fixed_probability for node in G.nodes()}

    activation_count = defaultdict(int)
    daily_sums = [0] * max_days

    for j in range(iterations):
        _, daily_retweeters, activated_nodes = ICM(G, seed_nodes, node_probabilities, max_days=max_days)
        for node in activated_nodes:
            activation_count[node] += 1
        for day in range(max_days):
            daily_sums[day] += daily_retweeters[day]

    top_10 = Counter(activation_count).most_common(10)
    average_retweets = [round(total / iterations, 2) for total in daily_sums]

    return top_10, average_retweets

#top_10, average_retweets = getTopActivatedNodes(Maxie_filepath, Maxie_seed, 0.005275, 14, 1000)

fixedProbability = 0.005275
average_retweets, average_viewers = getDailyRetweets(Maxie_filepath, Maxie_seed, fixedProbability, 14, 1000)

# print("Top 10 Most Frequently Activated Nodes")
# for rank, (node, count) in enumerate(top_10, 1):
#     print(f"{rank}. Node {node}: {count} activations")
# print("===============================================================")


#Le data

#Retweets
print("Retweets Analysis")
predicted = average_retweets
observed =  [1, 370,    10,   1,    2,   1, 0, 1, 0, 0, 0, 0, 0, 0]
print("===============================================================")
print("On Probability:", fixedProbability)
print(f"Average Retweets: {average_retweets}")
print(f"Observed Data: {observed}")
print("===============================================================")

rmse = root_mean_squared_error(observed, predicted)
r2 = r2_score(observed, predicted)
mean_observed = np.mean(observed)
normalized_rmse = rmse/mean_observed
mae = mean_absolute_error(observed, predicted)
print(f"RMSE: {rmse:.4f}")
print(f"R-squared: {r2:.4f}", f", Accuracy: {r2*100:.4f}")

print()
#Views
print("Viewers Analysis")
predicted = average_viewers
observed =  [1, 58000, 33000, 5000, 5000, 2000, 2000, 2000, 0, 0, 0, 0, 0, 0]
print("===============================================================")
print("On Probability:", fixedProbability)
print(f"Average Viewers: {average_viewers}")
print(f"Observed Data: {observed}")
print("===============================================================")

rmse = root_mean_squared_error(observed, predicted)
r2 = r2_score(observed, predicted)
mean_observed = np.mean(observed)
normalized_rmse = rmse/mean_observed
mae = mean_absolute_error(observed, predicted)
print(f"RMSE: {rmse:.4f}")
print(f"R-squared: {r2:.4f}", f", Accuracy: {r2*100:.4f}")



# Visualize the activated subgraph
# def visualize_activated_subgraph(G, activated_nodes):
#     pos = nx.spring_layout(G, seed=42)  # layout for consistent positioning

#     plt.figure(figsize=(10, 7))
#     nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, arrowsize=15)
#     plt.title("Activated Subgraph after Independent Cascade")
#     plt.show()

