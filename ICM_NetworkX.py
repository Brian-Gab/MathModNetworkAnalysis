import networkx as nx
import random
import matplotlib.pyplot as plt

fixedProbability = 0.005
Anji_filepath = "Networks/Anji_real.txt"
Maxie_filepath = "Networks/Maxie_real.txt"

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

    day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, day14 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for j in range(1, iterations+1):
        daily_viewers, daily_retweeters, activated_nodes = ICM(G, seed_nodes, node_probabilities, max_days=max_days)
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
    print("===============================================================")
    print("On Probability:", fixed_probability)
    print(f"Average Retweets: {averageRetweets}")
    print("===============================================================")
    return averageRetweets

def plotGraph(daily_viewers, averageRetweets):
    plt.figure(figsize=(10, 6))
    plt.plot(range(14), daily_viewers, marker='o', linestyle='-', color='blue', label="Viewers (Seen Tweet)")
    #plt.plot(range(14), averageRetweets, marker='s', linestyle='--', color='red', label="Retweeters (New RTs)")

    plt.xlabel("Days")
    plt.ylabel("Number of People")
    plt.title("Spread of Tweet Viewers and Retweeters Over 14 Days")
    plt.legend()
    plt.grid()
    plt.show()

getDailyRetweets(Maxie_filepath, ["maxieandreison"], fixedProbability, 14, 10000)






# Visualize the activated subgraph
# def visualize_activated_subgraph(G, activated_nodes):
#     pos = nx.spring_layout(G, seed=42)  # layout for consistent positioning

#     plt.figure(figsize=(10, 7))
#     nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, arrowsize=15)
#     plt.title("Activated Subgraph after Independent Cascade")
#     plt.show()

