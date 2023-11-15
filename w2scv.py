from getDepinfo import *
from chaoge import AtoA
from ltp import LTP, StnSplit


# 示例
semantic_roles = [{'predicate': '帮助', 'arguments': [('A0', '法律顾问'), ('A1', '联合部队指挥官及其参谋'), ('A2', '了解适用的国际条约、法规和所在国法律')]},
                  {'predicate': '了解', 'arguments': [('A0', '联合部队指挥官及其参谋'), ('A1', '适用的国际条约、法规和所在国法律')]},
                  {'predicate': '适用', 'arguments': [('A1', '国际条约、法规和所在国法律')]}]

result = process_semantic_roles(semantic_roles)
print(result)
if __name__ == '__main__':
    ltp = LTP("../base2")
    atoa = AtoA()
    txt_file_path = '../data/第一、二章'
    txt = atoa.getTxt(txt_file_path=txt_file_path + '.txt')
    sents = StnSplit().split(txt)
    #print(sents[0],sents[1])
    for sent in sents:
        result = ltp.pipeline(sent, tasks=["cws", "srl", 'ner', 'dep', 'pos'])
        #print(result.srl)
        triplesWithCoordination=process_semantic_roles(result.srl)
        #print(triplesWithCoordination)
        triples=atoa.getTripleWithoutCoordination(triplesWithCoordination)
        print(triples)
