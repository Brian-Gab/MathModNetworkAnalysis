import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error
import numpy as np

fixedProbability = 0.005257 #Probability
Maxie_filepath = "Networks/Maxie_real.txt" #Network
Maxie_seed = ["maxieandreison"] #Seed

def importGraph(filepath):
    print(f"Loading graph from {filepath}...")
    G = nx.DiGraph()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                followed, follower = parts[1], parts[0]
                G.add_edge(follower, followed)
    print(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    return G

def ICM(G, seed_nodes, node_probabilities, max_days=14):
    activated_nodes = set(seed_nodes)
    new_active = set(seed_nodes)
    daily_viewers = [len(new_active)]
    daily_retweeters = [len(new_active)]

    for day in range(1, max_days):
        next_active = set()
        viewers_today = set(new_active)

        for node in new_active:
            for neighbor in G.successors(node):
                if neighbor not in activated_nodes:
                    viewers_today.add(neighbor)
                    if random.random() < node_probabilities.get(neighbor, 0):
                        next_active.add(neighbor)

        activated_nodes.update(next_active)
        new_active = next_active

        daily_viewers.append(len(viewers_today))
        daily_retweeters.append(len(next_active))

    return daily_viewers, daily_retweeters, activated_nodes

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

fixedProbability = 0.005257
average_retweets, average_viewers = getDailyRetweets(Maxie_filepath, Maxie_seed, fixedProbability, 14, 10)

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
print(f"RMSE: {rmse:.4f}")
print(f"R-squared: {r2:.4f}", f", Accuracy: {r2*100:.4f}")