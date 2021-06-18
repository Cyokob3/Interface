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
        i += 1
        l[1] = str(i)
        corpus.append(l)
        time = []
    time = [(float((corpus[i][2])), corpus[i][1]) for i in range(len(corpus))]
    sort_time = sorted(time)
    t1 = [sort_time[i][1] for i in range(len(sort_time))]
    print(t1)
            
    

getcorpus()
