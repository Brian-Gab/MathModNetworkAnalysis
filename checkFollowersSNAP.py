import snap

print("Loading graph...")
G = snap.LoadEdgeList(snap.PNGraph, "Networks/Anji_test.txt", 0, 1)
print(f"Graph loaded with {G.GetNodes()} nodes and {G.GetEdges()} edges.")

def getFollowers(G):
    print("Checking indegrees...")
    in_degree_list = [(NI.GetId(), NI.GetInDeg()) for NI in G.Nodes()]
    most_followed_in = sorted(in_degree_list, key=lambda x: x[1], reverse=True)[:10]

    print("Top 10 most followed users (In-Degree):", most_followed_in)
    most_followed_node_in, followers_count_in = most_followed_in[0]
    print(f"Node: {most_followed_node_in}")
    print(f"Followers: {followers_count_in}")

    print()

    print("Checking outdegrees...")
    out_degree_list = [(NI.GetId(), NI.GetOutDeg()) for NI in G.Nodes()]
    most_followed_out = sorted(out_degree_list, key=lambda x: x[1], reverse=True)[:10]

    print("Top 10 most follwing users (Out-Degree):", most_followed_out)
    most_followed_node_out, followers_count_out = most_followed_out[0]
    print(f"Node: {most_followed_node_out}")
    print(f"Followings: {followers_count_out}")
    print()

def getFollowersOf(G, node):
    print(f"Checking followers for node {node}...")
    inDegree = G.GetNI(node).GetInDeg()

    print(f"Node {node} has {inDegree} followers.")
    return inDegree

getFollowersOf(G, 0)