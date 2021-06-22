def getcorpus():
    fname = "/Users/sugimotoyoshiki/prog/python/Interface/data/G3.txt"
    i = 0
    corpus = []
    if fname == '': return
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        l = line.split("\t")
        l.pop(1)
        corpus.append(l)
    print(sorted(corpus, key=lambda x:float(x[1])))
    
    

getcorpus()
