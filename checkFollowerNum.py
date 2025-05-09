import networkx as nx

G = nx.DiGraph()
print("Loading Anji's graph...")
with open("Networks/Anji_real.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) == 2:
            followed, follower = parts[0], parts[1]
            G.add_edge(follower, followed)  # B → A (follower → followed)
print(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

# Compute in-degree and out-degree
print("Checking indegrees...")
in_degree_list = [(node, deg) for node, deg in G.in_degree()]
print("Checking outdegrees...")
out_degree_list = [(node, deg) for node, deg in G.out_degree()]

# Sort and get top 10
print("Sorting...")
most_followed_in = sorted(in_degree_list, key=lambda x: x[1], reverse=True)[:10]
most_followed_out = sorted(out_degree_list, key=lambda x: x[1], reverse=True)[:10]

# Output results
print("===============================================================")
print("Top 10 most followed users (In-Degree):", most_followed_in)
print("Top 10 most active followers (Out-Degree):", most_followed_out)
print()
print("===============================================================")

print("===============================================================")
if most_followed_in:
    most_followed_node_in, followers_count_in = most_followed_in[0]
    print(f"Node: {most_followed_node_in}")
    print(f"Followers: {followers_count_in}")
    print()

if most_followed_out:
    most_followed_node_out, followers_count_out = most_followed_out[0]
    print(f"Node: {most_followed_node_out}")
    print(f"Followings: {followers_count_out}")
print("===============================================================")