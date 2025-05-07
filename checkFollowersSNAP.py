import snap

G = snap.LoadEdgeList(snap.PNGraph, "Networks/test.csv", 0, 1)

print("Checking indegrees...")
in_degree_list = [(NI.GetId(), NI.GetInDeg()) for NI in G.Nodes()]

print("Checking outdegrees...")
out_degree_list = [(NI.GetId(), NI.GetOutDeg()) for NI in G.Nodes()]

most_followed_in = sorted(in_degree_list, key=lambda x: x[1], reverse=True)[:10]
most_followed_out = sorted(out_degree_list, key=lambda x: x[1], reverse=True)[:10]

print("Top 10 most followed users (In-Degree):", most_followed_in)
print("Top 10 most followed users (Out-Degree):", most_followed_out)
print()

most_followed_node_in, followers_count_in = most_followed_in[0]
print(f"Node: {most_followed_node_in}")
print(f"Followers: {followers_count_in}")
print()

most_followed_node_out, followers_count_out = most_followed_out[0]
print(f"Node: {most_followed_node_out}")
print(f"Following: {followers_count_out}")