import snap
import random
import sys

# Step 1: Create a Directed Graph
G = snap.TNGraph.New()

# Root node (influencer)
root_node = 0
G.AddNode(root_node)

# Add follower nodes
num_followers = 58000
followers = list(range(1, num_followers + 1))

print("Adding followers...")
for i in followers:
    G.AddNode(i)
    G.AddEdge(i, root_node)  # Directly add edge

print(f"Base graph created with {G.GetNodes()} nodes and {G.GetEdges()} edges.")

# Step 2: Add connections
existing_nodes = set(followers)
next_available_id = num_followers + 1
second_level_followers = []

# Select 100–200 special followers with 2,000+ children
num_special = random.randint(100, 200)
special_followers = set(random.sample(followers, num_special))

progress_interval = 1000

for i, follower in enumerate(followers, 1):
    try:
        # If special, assign at least 2000 children
        if follower in special_followers:
            num_children = random.randint(2000, 2500)
        else:
            num_children = random.randint(10, 300)

        children = range(next_available_id, next_available_id + num_children)
        next_available_id += num_children

        for child in children:
            G.AddNode(child)
            G.AddEdge(child, follower)
            existing_nodes.add(child)
            second_level_followers.append(child)

        # Add sibling connections
        num_siblings = random.randint(1, 10)
        if num_siblings > 0:
            siblings = random.sample(followers, num_siblings)
            for sibling in siblings:
                G.AddEdge(follower, sibling)

        if i % progress_interval == 0:
            print(f"Processed {i}/{num_followers} followers...")
            sys.stdout.flush()

    except Exception as e:
        print(f"\nError at follower {i} ({follower}): {str(e)}")
        raise

print(f"\nCompleted! Final stats: Nodes: {G.GetNodes()}, Edges: {G.GetEdges()}")

# Step 3: Save Graph as Edge List
print("Saving graph...")
snap.SaveEdgeList(G, "Networks/test.csv")
print("Edge list exported!")