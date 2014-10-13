from sys import argv
import networkx as nx
import praw
import matplotlib.pyplot as plt

def expand_tup(tup):
    out = []
    for x in range(0,len(tup)):
        for y in range(x+1,len(tup)):
            out.append((tup[x],tup[y]))
    return out

if len(argv)>1:
    subsfile = argv[1]
else:
    subsfile = "subreddits.txt"

with open(subsfile) as f:
    subs = f.read().splitlines()
#subs = ["askreddit",
#        "announcements",
#        "todayilearned",
#        "blog",
#        "worldnews",
#        "gaming",
#        "science",
#        "blog",
#        "bestof",
#        "videos",
#        "Iama",
#        "askscience",
#        "cringepics",
#        "pics",
#        "funny"]


# mods = {"robert" ("askreddit","Iama"), "james": ("Iama","askscience","pics")}
mods = {}

r=praw.Reddit(user_agent=("Subreddit shared mods thing"))
# G=nx.Graph()
G=nx.Graph()
for x in subs:
    G.add_node(x)

if "read" not in argv:
    for sub in subs:
        print sub
        for user in r.get_subreddit(sub).get_moderators():
            user = user.name
            if user in mods:
                mods[user].append(sub)
            else:
                mods[user]=[sub]
    del mods["AutoModerator"]
    with open("save.txt","w") as f:
        f.write(str(mods))
else:
    with open("save.txt") as f:
        mods = eval(f.read())

for mod in mods:
    if len(mods[mod])>10: print mod,mods[mod]
    if len(mods[mod])<10:
        mods[mod]=[]

for mod in mods.keys():
    G.add_edges_from(expand_tup(mods[mod]))
print "Subreddits",G.nodes()
pos = nx.spring_layout(G,iterations=200,k=1.5)
# pos = nx.(G)
# nx.draw(G,pos,node_color=[[0,0.9,0.9]],node_size=[400*len(x) for x in G.nodes()],cmap=plt.cm.Blues)
nx.draw(G,pos,node_color=[[0,0.9,0.9]],node_size=1000,cmap=plt.cm.Blues,width=0.5,
        label="Subreddits with shared moderators",
        fontsize=5)
plt.show()

