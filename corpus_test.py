import collections
import MeCab
import csv


def main():
    files = ['G1','G2','G3','G4','G6','G7','G8','G9','G10','G11']
    # 初期化
    count_collection = []
    count = []
    corpus = []
    data = []
    menber = []
    index_id = 0
    i = 0
    m = MeCab.Tagger("-Osimple -u user.dic")

    target_menber = 'oll'
    target_wclass = 'meisi'


    for fname in files:
        count_collection = []
        count = []
        corpus = []
        data = []
        menber = []
        index_id = 0
        i = 0
        f = open('/Users/sugimotoyoshiki/prog/python/data/' + fname + '.txt','r')
        lines = f.readlines()
        f.close()
        for line in lines:
            l = line.split("\t")
            i += 1
            l.pop(1)
            l.insert(0, i)
            menber.append(l[1])
            data.append(l)
        menber = sorted(set(menber))
        data = sorted(data, key=lambda x:float(x[2]))

        for x in data:
            if target_menber in 'oll':
                convert = m.parse(x[5]).splitlines()
            elif target_menber in x[1]:
                convert = m.parse(x[5]).splitlines()
            else : continue
            line_id = x[0]
            for y in convert:
                convert_split = y.split('\t')
                convert_split.insert(0, line_id)
                corpus.append(convert_split)
            
        for corpus_element in corpus:
            if 'EOS' in corpus_element[1]: continue
            if '-' in corpus_element[2]:
                w = corpus_element[2].split("-")
            else : w = [corpus_element[2]]
            if target_wclass in 'oll': 
                count_collection.append(corpus_element[1])
                continue
            if target_wclass in w[0]:
                count_collection.append(corpus_element[1])
                print(corpus_element)
        count_collection = collections.Counter(count_collection)
        for turn in range(len(set(count_collection))):
            count.append(count_collection.most_common()[turn])

        with open('/Users/sugimotoyoshiki/prog/python/data/' + fname + '.csv',encoding="cp932",mode='w') as f:
            writer = csv.writer(f)
            writer.writerows(count)

 
main()