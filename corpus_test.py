#class Textcorpus():

def getcorpus():
    fname = "/Users/sugimotoyoshiki/prog/python/Interface/data/G3.txt"
    if fname == '': return
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        l = [line.strip() for line in line.split("\t")]
        #print(l[2])
        print(l)

getcorpus()
