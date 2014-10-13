from sys import argv
import networkx as nx
import praw #Reddit API library
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
MINSUB = 4
MAXLEN = 9
mods = {}
inmods=[]
insubs=[]

r=praw.Reddit(user_agent=("Subreddit shared mods thing"))
# G=nx.Graph()
G=nx.Graph()
#for x in subs:
#    G.add_node(x)
#    insubs.append(x)

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
    if len(mods[mod])>=MINSUB:
        print mod,mods[mod]
        G.add_node(mod[0:MAXLEN])
        inmods.append(mod[0:MAXLEN])
    else:
        mods[mod]=[]

for mod in mods.keys():
    for sub in mods[mod]:
        G.add_edge(mod[0:MAXLEN],sub[0:MAXLEN])
        if sub not in insubs: insubs.append(sub[0:MAXLEN])
print "----------------------------------------------"
print "Subreddits",G.nodes()
print "----------------------------------------------"
print insubs
print inmods
print "----------------------------------------------"
pos = nx.shell_layout(G,scale=1.5,nlist=[inmods,insubs])
print pos
nx.draw(G,pos,node_color=[[0,0.9,0.9]],node_size=4000,cmap=plt.cm.Blues,width=0.5,
        label="Subreddits with shared moderators",
        fontsize=4)
plt.show()

