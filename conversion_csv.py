import collections
import MeCab
import csv

ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))

ZEN2HAN = str.maketrans(ZEN, HAN)
HAN2ZEN = str.maketrans(HAN, ZEN)




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
    total = []
    t = []
    m = MeCab.Tagger("-Ochasen -u user.dic")

    target_menber = 'oll'
    #target_wclass = ['名詞','一般']
    target_wclass = '動詞'
    patten = '2'
    oll = []
    oll_a = []
    for fname in files:
        count_collection = []
        count = []
        corpus = []
        data = []
        menber = []
        cw = 0
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
            regular = x[5]
            regular = regular.translate(ZEN2HAN)
            if target_menber in 'oll':
                convert = m.parse(regular).splitlines()
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
            if '?' in corpus_element[1]: continue
            if ':' in corpus_element[1]: continue
            if '.' in corpus_element[1]: continue
            if '=' in corpus_element[1]: continue
            if '(' in corpus_element[1]: continue
            if ')' in corpus_element[1]: continue
            if '。' in corpus_element[1]: continue
            if '、' in corpus_element[1]: continue
            if 'Lol' in corpus_element[1]: continue
            
            if '-' in corpus_element[4]:
                w = corpus_element[4].split("-")
            else : w = [corpus_element[4]]
            
            
            #if '名詞' in w[0]: continue
            #if '動詞' in w[0]: continue
            #if '形容詞' in w[0]: continue
            #if '助詞' in w[0]: continue
            #if '助動詞' in w[0]: continue
            #if 'フィラー' in w[0]: continue
            #if '感動詞' in w[0]: continue

            if patten == '1':
                if target_wclass in 'oll': 
                    count_collection.append(corpus_element[4])
                    oll.append(corpus_element[4])
                    cw += 1
                    continue

            if patten == '2':
                if target_wclass == w[0]:
                    # count_collection.append(corpus_element[1])
                    count_collection.append(corpus_element[1])
                    oll.append(corpus_element[4])
                    print(corpus_element)
                    cw += 1

            if patten == '3':
                if target_wclass in 'oll': 
                    count_collection.append(corpus_element[1])
                    print(corpus_element)
                    cw += 1
                    continue

            if patten == '4':
                if target_wclass in corpus_element[4]:
                    count_collection.append(corpus_element[1])
                    oll.append(corpus_element[4])
                    print(corpus_element)
                    cw += 1

        count_collection = collections.Counter(count_collection)
        t.append(len(set(count_collection)))
        for turn in range(len(set(count_collection))):
            count.append(count_collection.most_common()[turn])
        with open('/Users/sugimotoyoshiki/prog/python/data/' + fname + '.csv',encoding="cp932",mode='w') as f:
            writer = csv.writer(f)
            writer.writerows(count)
        total.append(cw)
    print('種類数 : ' + str(t))
    print('単語数 : ' + str(total))
    print('合計 : ' + str(sum(total)))
    oll = collections.Counter(oll)
    for turn in range(len(set(oll))):
        print(oll.most_common()[turn])
        oll_a.append(oll.most_common()[turn])
    with open('/Users/sugimotoyoshiki/prog/python/data/'+ 'oll.csv',encoding="cp932",mode='w') as f:
        writer = csv.writer(f)
        writer.writerows(oll_a)

 
main()