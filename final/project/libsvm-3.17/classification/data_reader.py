from pickle import load, dump


f = open("good_plants", 'r')
contents = load(f)
contents = contents[:20000]
g = open("good_plants_small", 'w')
dump(contents, g)
f.close()
g.close()


f = open("bad_plants", 'r')
contents = load(f)
contents = contents[:45000]
g = open("bad_plants_small", 'w')
dump(contents, g)
f.close()
g.close()

