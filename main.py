from ltp import LTP, StnSplit
from tqdm import tqdm

from AtoA import AtoA
from getDepinfo import *

# 示例
semantic_roles = [{'predicate': '帮助', 'arguments': [('A0', '法律顾问'), ('A1', '联合部队指挥官及其参谋'),
                                                      ('A2', '了解适用的国际条约、法规和所在国法律')]},
                  {'predicate': '了解',
                   'arguments': [('A0', '联合部队指挥官及其参谋'), ('A1', '适用的国际条约、法规和所在国法律')]},
                  {'predicate': '适用', 'arguments': [('A1', '国际条约、法规和所在国法律')]}]

result = process_semantic_roles(semantic_roles)
# print(result)

if __name__ == '__main__':
    ltp = LTP("../base2")
    atoa = AtoA(ltp)
    txt_file_path = '../data/第一、二章'
    txt = atoa.getTxt(txt_file_path=txt_file_path + '.txt')
    sents = StnSplit().split(txt)

    # print(sents[0],sents[1])
    '''test = [[' 本出版物‘,’阐述', '对抗全过程中在电磁频谱以及通过电磁频谱展开的军事行动', '_', '_'],
            ['司令部', '_', '和', '_', '0'], ['职责', '_', '和', '_', '0']]'''
    # atoa.triple2csv(csv_file_path='../data/mainoutput.csv',tripleList=test)
    output = []
    for sent in tqdm(sents, position=0):
        result = ltp.pipeline(sent, tasks=["cws", "srl", 'ner', 'dep', 'pos'])
        # print(result.srl)
        triplesWithCoordination = process_semantic_roles(result.srl)
        # print(triplesWithCoordination)
        triples = atoa.getTripleWithoutCoordination(triplesWithCoordination)
        # print(triples)
        output.extend(triples)
    atoa.triple2csv(csv_file_path='../data/mainoutput.csv', tripleList=output)
    atoa.assign_numbers(input_file='../data/mainoutput.csv', output_file='../data/mainoutputassign_numbers.csv',
                        current_number=atoa.COOnumber)
    uri = "bolt://localhost:7687"  # 替换为你的Neo4j数据库URI
    username = "neo4j"  # 替换为你的数据库用户名
    password = "12345678"
    name = 'neo4j1113'
    atoa.create_graph_from_csv(csv_file='../data/mainoutputassign_numbers.csv', uri=uri, username=username,
                               password=password, name=name, deleteAll=True)

    # print(sents[0],sents[1])
    for sent in sents:
        result = ltp.pipeline(sent, tasks=["cws", "srl", 'ner', 'dep', 'pos'])
        # print(result.srl)
        triplesWithCoordination = process_semantic_roles(result.srl)
        # print(triplesWithCoordination)
        triples = atoa.getTripleWithoutCoordination(triplesWithCoordination)
        print(triples)
